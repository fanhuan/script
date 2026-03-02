#!/usr/bin/env python3
import argparse
import pysam
import sys

MAX_BAM_POS = 2_147_483_647  # BAM 32-bit signed coord limit (0-based internal)

def parse_args():
    p = argparse.ArgumentParser(
        description="Remap BAM coords to a single concatenated contig with fixed spacers (strict & safe)."
    )
    p.add_argument("in_bam", help="Input BAM (name- or coord-sorted).")
    p.add_argument("out_bam", help="Output BAM on single concatenated contig.")
    p.add_argument("--contig-name", default="concat", help="Name of the concatenated contig.")
    p.add_argument("--spacer", type=int, default=500, help="Spacer size between chromosomes (bp).")
    p.add_argument("--keep-chr-order-from", choices=["header","alpha"], default="header",
                   help="Use SQ order from header (default) or alphabetical.")
    p.add_argument("--keep-unmapped", action="store_true",
                   help="Write unmapped reads through unchanged (default: drop them).")
    return p.parse_args()

def collect_sqs(hdr, order_mode):
    sqs = hdr.get("SQ", [])
    if not sqs:
        raise RuntimeError("Input BAM header has no @SQ lines.")
    pairs = [(sq["SN"], int(sq["LN"])) for sq in sqs]
    if order_mode == "alpha":
        pairs.sort(key=lambda x: x[0])
    return pairs

def build_offsets(sq_pairs, spacer):
    offsets = {}
    pads = []
    running = 0
    for i, (name, ln) in enumerate(sq_pairs):
        offsets[name] = running
        running += ln
        if i != len(sq_pairs) - 1 and spacer > 0:
            pads.append((running, running + spacer))
            running += spacer
    total_len = running
    return offsets, pads, total_len

def rewrite_sa_tag(sa, offsets, new_rname):
    # SA:Z:rname,pos,strand,cigar,mapQ,NM;...
    parts = sa.rstrip(";").split(";")
    out_parts = []
    for entry in parts:
        if not entry:
            continue
        f = entry.split(",")
        if len(f) < 6:
            out_parts.append(entry); continue
        rname, pos1 = f[0], f[1]
        try:
            pos1_i = int(pos1)  # 1-based
        except ValueError:
            out_parts.append(entry); continue
        off = offsets.get(rname)
        if off is None:
            # Keep as-is but this shouldn't happen if header is consistent
            out_parts.append(entry); continue
        new_pos1 = off + (pos1_i - 1) + 1
        f[0] = new_rname
        f[1] = str(new_pos1)
        out_parts.append(",".join(f))
    return ";".join(out_parts) + ";"

def main():
    args = parse_args()

    in_bam = pysam.AlignmentFile(args.in_bam, "rb")
    sq_pairs = collect_sqs(in_bam.header.to_dict(), args.keep_chr_order_from)

    # Build offsets & sanity-check contig length limit
    offsets, pads, total_len = build_offsets(sq_pairs, args.spacer)
    if total_len > MAX_BAM_POS:
        raise RuntimeError(
            f"Concatenated contig length {total_len:,} exceeds BAM coordinate limit {MAX_BAM_POS:,}. "
            f"Use a tiled output (multiple contigs) instead."
        )

    # New header: single @SQ
    new_header = in_bam.header.to_dict()
    new_header["SQ"] = [{"SN": args.contig_name, "LN": total_len}]
    chrom_order = [n for n, _ in sq_pairs]
    chrom_lengths = dict(sq_pairs)
    comp = []
    for i, cname in enumerate(chrom_order):
        comp.append(f"{cname}:len={chrom_lengths[cname]},off={offsets[cname]}")
        if i != len(chrom_order) - 1 and args.spacer > 0:
            s, e = pads[i]
            comp.append(f"[PAD {args.spacer}bp @ {s}-{e})")
    new_header.setdefault("CO", []).append(
        f"Concatenated {args.contig_name} from: " + " | ".join(comp)
    )

    out_bam = pysam.AlignmentFile(args.out_bam, "wb", header=new_header)
    new_tid = out_bam.get_tid(args.contig_name)

    # Pre-map for quick membership tests
    all_refs = set(chrom_order)

    try:
        for rec in in_bam.fetch(until_eof=True):
            # Unmapped handling
            if rec.is_unmapped:
                if args.keep_unmapped:
                    out_bam.write(rec)
                continue

            old_rname = in_bam.get_reference_name(rec.reference_id)
            if old_rname not in all_refs:
                raise RuntimeError(
                    f"Read {rec.query_name} maps to reference '{old_rname}' that is not in @SQ. "
                    "Input BAM/header mismatch."
                )

            # Shift primary
            off = offsets[old_rname]
            new_pos0 = off + rec.reference_start  # 0-based
            if new_pos0 < 0 or new_pos0 > MAX_BAM_POS:
                raise RuntimeError(
                    f"Shifted position exceeds BAM limit: {old_rname}:{rec.reference_start+1} -> {new_pos0+1}"
                )
            rec.reference_id = new_tid
            rec.reference_start = new_pos0

            # Mate
            orig_mate_same_chrom = False
            if not rec.mate_is_unmapped:
                mate_rname = rec.next_reference_name
                if mate_rname not in all_refs:
                    raise RuntimeError(
                        f"Mate of {rec.query_name} on '{mate_rname}' missing from @SQ."
                    )
                rec.next_reference_id = new_tid
                rec.next_reference_start = offsets[mate_rname] + rec.next_reference_start
                if mate_rname == old_rname:
                    orig_mate_same_chrom = True

            # TLEN policy
            if rec.mate_is_unmapped or not orig_mate_same_chrom:
                rec.template_length = 0

            # SA tag
            if rec.has_tag("SA"):
                sa_new = rewrite_sa_tag(rec.get_tag("SA"), offsets, args.contig_name)
                rec.set_tag("SA", sa_new, value_type="Z")

            out_bam.write(rec)
    finally:
        in_bam.close()
        out_bam.close()

if __name__ == "__main__":
    main()

