#!/usr/bin/env python3
"""postprocess_braker_gtf.py

Post-process a BRAKER GTF so strict downstream tools (notably SnpEff's database
build) read it correctly. Three independent cleanups, each ON by default and
individually switch-off-able:

  1. FILL PARENT IDs
     AUGUSTUS/BRAKER writes `gene` and `transcript` lines with a *bare* id in
     column 9, e.g.

         chr1  AUGUSTUS  gene        11802  53495  .  -  .  g1
         chr1  AUGUSTUS  transcript  13224  53351  .  -  .  g1.t1

     instead of the standard `key "value";` format the child features use.
     Strict parsers cannot read an id off these lines; SnpEff then synthesises
     coordinate-based placeholder markers (GENE_chr_start_end,
     TRANSCRIPT_chr_start_end wrapped in null.N genes), duplicating every locus
     as phantom `intragenic_variant` / `pseudogene` records. This rewrites the
     bare lines into proper `gene_id "..."; transcript_id "...";` attributes.

  2. DROP REDUNDANT mRNA LINES                                    [--keep-mrna]
     BRAKER emits, for each GeneMark.hmm3 transcript, a second parent line of
     type `mRNA` in addition to its `transcript` line (same transcript_id).
     When stringtie2utr adds UTRs it extends the `gene`/`transcript` lines but
     leaves the `mRNA` line at its original coding-only span, so the `mRNA`
     line carries stale, pre-UTR coordinates that conflict with the real
     transcript. The `transcript` line plus the exon/CDS/UTR children already
     define the model, so the redundant `mRNA` lines are dropped (only when a
     `transcript` line with the same id exists, so nothing is orphaned).

  3. DROP GENE-DISRUPTING UTRs                                 [--keep-bad-utr]
     stringtie2utr (including the current official BRAKER4 version) can relabel
     a StringTie exon that falls *inside* a BRAKER intron as a 5'/3' UTR, with
     no check that it lies outside the coding region. The result is a UTR
     sitting in the middle of the CDS. SnpEff then treats the coding sequence
     as starting only after that 5' UTR, shifts the reading frame, and reports
     WARNING_TRANSCRIPT_MULTIPLE_STOP_CODONS plus a spurious missense call.
     A legitimate UTR lies entirely outside its transcript's CDS span, so this
     drops any UTR feature that overlaps the [min CDS start, max CDS end] span
     of its transcript. Correctly-placed flanking UTRs are kept.

WHAT IT DOES *NOT* DO
     Every other line is written back unchanged, preserving order and
     formatting. Parent-line spans are not recomputed (SnpEff rebuilds
     transcript bounds from the exon/CDS children anyway). It is idempotent:
     re-running a cleaned file is a no-op.

USAGE
     postprocess_braker_gtf.py input.gtf output.gtf
     postprocess_braker_gtf.py input.gtf > output.gtf       # output -> stdout
     cat input.gtf | postprocess_braker_gtf.py - -          # stdin -> stdout
     postprocess_braker_gtf.py --keep-mrna --keep-bad-utr in.gtf out.gtf

No third-party dependencies (standard library only).
"""

import argparse
import re
import sys

GENE_ID_RE = re.compile(r'gene_id\s+"([^"]+)"')
TX_ID_RE = re.compile(r'transcript_id\s+"([^"]+)"')
UTR_TYPES = ("five_prime_UTR", "three_prime_UTR")


def open_in(path):
    return sys.stdin if path == "-" else open(path)


def open_out(path):
    return sys.stdout if path in ("-", None) else open(path, "w")


def bare_id(attr):
    """Extract the bare identifier from an AUGUSTUS-style attribute column."""
    return attr.strip().strip('"').rstrip(";").strip()


def postprocess(lines, drop_mrna=True, drop_bad_utr=True):
    # ---- Pass 1: per-transcript CDS span, and the set of transcript ids that
    # have a `transcript` line (needed to safely drop duplicate mRNA lines). ----
    cds_min, cds_max = {}, {}
    tx_line_ids = set()
    for line in lines:
        if not line.strip() or line.startswith("#"):
            continue
        f = line.rstrip("\n").split("\t")
        if len(f) != 9:
            continue
        ftype = f[2]
        if ftype == "transcript":
            m = TX_ID_RE.search(f[8])
            tx_line_ids.add(m.group(1) if m else bare_id(f[8]))
        elif ftype == "CDS":
            m = TX_ID_RE.search(f[8])
            if m:
                tid, s, e = m.group(1), int(f[3]), int(f[4])
                if tid not in cds_min or s < cds_min[tid]:
                    cds_min[tid] = s
                if tid not in cds_max or e > cds_max[tid]:
                    cds_max[tid] = e

    # ---- Pass 2: emit with the three cleanups applied. ----
    out = []
    current_gene = None
    n = dict(gene_fixed=0, tx_fixed=0, tx_no_gene=0,
             mrna_dropped=0, mrna_kept=0, utr_dropped=0, utr_no_span=0)

    for line in lines:
        if not line.strip() or line.startswith("#"):
            out.append(line)
            continue
        f = line.rstrip("\n").split("\t")
        if len(f) != 9:
            out.append(line)
            continue

        ftype, attr = f[2], f[8]

        if ftype == "gene":
            m = GENE_ID_RE.search(attr)
            if m:                                      # already proper
                current_gene = m.group(1)
                out.append(line)
            else:                                      # bare id -> rewrite
                gid = bare_id(attr)
                current_gene = gid
                f[8] = 'gene_id "{}";'.format(gid)
                out.append("\t".join(f) + "\n")
                n["gene_fixed"] += 1

        elif ftype == "transcript":
            mt = TX_ID_RE.search(attr)
            if mt and GENE_ID_RE.search(attr):         # already proper
                out.append(line)
            else:                                      # bare id -> rewrite
                tid = bare_id(attr)
                if current_gene is not None:
                    gid = current_gene
                else:                                  # fall back: gN.tM -> gN
                    gid = tid.rsplit(".", 1)[0]
                    n["tx_no_gene"] += 1
                f[8] = 'transcript_id "{}"; gene_id "{}";'.format(tid, gid)
                out.append("\t".join(f) + "\n")
                n["tx_fixed"] += 1

        elif ftype == "mRNA" and drop_mrna:
            m = TX_ID_RE.search(attr)
            if m and m.group(1) in tx_line_ids:        # redundant duplicate
                n["mrna_dropped"] += 1
                continue
            n["mrna_kept"] += 1                        # no transcript line -> keep
            out.append(line)

        elif ftype in UTR_TYPES and drop_bad_utr:
            m = TX_ID_RE.search(attr)
            tid = m.group(1) if m else None
            if tid is not None and tid in cds_min:
                us, ue = int(f[3]), int(f[4])
                if us <= cds_max[tid] and ue >= cds_min[tid]:   # overlaps CDS span
                    n["utr_dropped"] += 1
                    continue
                out.append(line)                       # flanking UTR -> keep
            else:
                n["utr_no_span"] += 1                  # no CDS to judge -> keep
                out.append(line)

        else:
            out.append(line)

    return out, n


def main():
    ap = argparse.ArgumentParser(
        description="Post-process a BRAKER GTF: fill bare parent IDs, drop "
                    "redundant mRNA lines, and drop UTRs that overlap the CDS.")
    ap.add_argument("input", help="input GTF (use '-' for stdin)")
    ap.add_argument("output", nargs="?", default="-", help="output GTF (default: stdout)")
    ap.add_argument("--keep-mrna", action="store_true",
                    help="keep the redundant GeneMark mRNA lines (default: drop them)")
    ap.add_argument("--keep-bad-utr", action="store_true",
                    help="keep UTRs that overlap the CDS span (default: drop them)")
    args = ap.parse_args()

    fin = open_in(args.input)
    try:
        lines = fin.readlines()
    finally:
        if fin is not sys.stdin:
            fin.close()

    out, n = postprocess(lines, drop_mrna=not args.keep_mrna,
                         drop_bad_utr=not args.keep_bad_utr)

    fout = open_out(args.output)
    try:
        fout.writelines(out)
    finally:
        if fout is not sys.stdout:
            fout.close()

    sys.stderr.write("Filled {} gene lines and {} transcript lines.\n".format(
        n["gene_fixed"], n["tx_fixed"]))
    if not args.keep_mrna:
        sys.stderr.write("Dropped {} redundant mRNA lines.\n".format(n["mrna_dropped"]))
    if not args.keep_bad_utr:
        sys.stderr.write("Dropped {} UTR lines overlapping the CDS span.\n".format(
            n["utr_dropped"]))
    if n["mrna_kept"]:
        sys.stderr.write("Warning: kept {} mRNA line(s) with no matching transcript "
                         "line.\n".format(n["mrna_kept"]))
    if n["tx_no_gene"]:
        sys.stderr.write("Warning: {} transcript line(s) had no preceding gene line; "
                         "gene_id derived from transcript_id.\n".format(n["tx_no_gene"]))


if __name__ == "__main__":
    main()
