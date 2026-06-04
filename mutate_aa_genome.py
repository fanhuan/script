#!/usr/bin/env python3
"""
mutate_aa_genome.py
-------------------
Annotate variants against a WHOLE-GENOME annotation and return the mutated
amino-acid sequence(s). You point it at:

  --gtf  whole-genome GTF (CDS features)
  --cds  genome-wide CDS FASTA   (one record per transcript)
  --aa   genome-wide protein FASTA (optional; used for validation)

...and give it one variant or a file of variants. The tool indexes the GTF
once, finds every transcript whose CDS overlaps each variant, edits that
transcript's CDS, and re-translates. No per-gene file prep needed.

Variants are on the FORWARD genome strand (VCF convention): CHROM_POS_REF_ALT.

Pure standard library (no Biopython), so it runs on any node.

Scope note: for annotating an entire multi-million-variant VCF, a production
tool (VEP, SnpEff, `bcftools csq`) is the right hammer. This script shines for
targeted sets (a gene, a candidate list, validation work) where you want a
transparent, hackable answer AND the actual mutant protein FASTA.
"""

import argparse
import sys
import textwrap

# ----------------------------------------------------------------------------
# Standard genetic code (NCBI table 1). '*' = stop.
# ----------------------------------------------------------------------------
STANDARD_CODE = {
    'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L', 'CTT': 'L', 'CTC': 'L',
    'CTA': 'L', 'CTG': 'L', 'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V', 'TCT': 'S', 'TCC': 'S',
    'TCA': 'S', 'TCG': 'S', 'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T', 'GCT': 'A', 'GCC': 'A',
    'GCA': 'A', 'GCG': 'A', 'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
    'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q', 'AAT': 'N', 'AAC': 'N',
    'AAA': 'K', 'AAG': 'K', 'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W', 'CGT': 'R', 'CGC': 'R',
    'CGA': 'R', 'CGG': 'R', 'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
}
COMPLEMENT = str.maketrans('ACGTNacgtn', 'TGCANtgcan')
BIN = 100_000   # genomic binning resolution for the point-overlap index


def revcomp(seq):
    return seq.translate(COMPLEMENT)[::-1]


def translate(nt, code=STANDARD_CODE, to_stop=True):
    nt = nt.upper().replace('U', 'T')
    aa = []
    for i in range(0, len(nt) - len(nt) % 3, 3):
        residue = code.get(nt[i:i + 3], 'X')
        if residue == '*' and to_stop:
            aa.append('*')
            break
        aa.append(residue)
    return ''.join(aa)


# ----------------------------------------------------------------------------
# FASTA reading
# ----------------------------------------------------------------------------
def read_fasta_dict(path):
    """Whole multi-record FASTA -> {first_token_of_header: sequence}."""
    d, key, buf = {}, None, []
    with open(path) as fh:
        for line in fh:
            if line.startswith('>'):
                if key is not None:
                    d[key] = ''.join(buf).upper().replace('U', 'T')
                key = line[1:].split()[0]
                buf = []
            elif line.strip():
                buf.append(line.strip())
    if key is not None:
        d[key] = ''.join(buf).upper().replace('U', 'T')
    return d


def lookup_seq(d, *keys):
    """Look up a sequence by any of several keys, with version-suffix
    tolerance (Foo.1 <-> Foo)."""
    for k in keys:
        if k and k in d:
            return d[k]
    for k in keys:
        if not k:
            continue
        base = k.rsplit('.', 1)[0]
        if base in d:
            return d[base]
        for cand in (k, base):              # match d-keys ignoring their version
            for dk in d:
                if dk.rsplit('.', 1)[0] == cand:
                    return d[dk]
    return None


# ----------------------------------------------------------------------------
# Variant parsing
# ----------------------------------------------------------------------------
def parse_variant(s):
    """'chr2_12345_AG_A' -> ('chr2', 12345, 'AG', 'A'). rsplit so scaffold
    names containing '_' survive."""
    parts = s.rsplit('_', 3)
    if len(parts) != 4:
        raise ValueError(f"'{s}' is not CHROM_POS_REF_ALT")
    chrom, pos, ref, alt = parts
    return chrom, int(pos), ref.upper(), alt.upper()


def iter_variants(path):
    """Yield (chrom, pos, ref, alt) from a file. Accepts:
       - CHROM_POS_REF_ALT per line
       - whitespace/tab CHROM POS REF ALT
       - VCF (skips headers, splits multiallelic ALT)."""
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            toks = line.split()
            if len(toks) == 1 and '_' in toks[0]:          # CHROM_POS_REF_ALT
                yield parse_variant(toks[0])
                continue
            f = line.split('\t') if '\t' in line else toks
            if len(f) >= 5:                                # VCF: CHROM POS ID REF ALT
                chrom, pos, ref = f[0], int(f[1]), f[3].upper()
                for a in f[4].upper().split(','):          # split multiallelic
                    yield chrom, pos, ref, a
            elif len(f) == 4:                              # CHROM POS REF ALT
                yield f[0], int(f[1]), f[2].upper(), f[3].upper()
            else:
                raise ValueError(f"Cannot parse variant line: {line!r}")


# ----------------------------------------------------------------------------
# GTF parsing -> transcript table + binned overlap index
# ----------------------------------------------------------------------------
def parse_attr(attr, key):
    for chunk in attr.strip().split(';'):
        chunk = chunk.strip()
        if not chunk:
            continue
        if chunk.startswith(key + ' ') or chunk.startswith(key + '"'):
            return chunk[len(key):].strip().strip('"').strip()
        if chunk.startswith(key + '='):
            return chunk[len(key) + 1:].strip().strip('"')
    return None


def build_index(gtf_path):
    """Parse the genome GTF once.
    Returns (transcripts, index):
      transcripts[tx] = {chrom, strand, gene_id, protein_id,
                         feats: [{start,end,phase,cum}], cds_len}
      index[chrom][bin_id] = [(start, end, tx), ...]   (CDS features)
    """
    raw = {}      # tx -> list of (start,end,phase)
    meta = {}     # tx -> (chrom,strand,gene_id,protein_id)
    n = 0
    for line in open(gtf_path):
        if line.startswith('#') or not line.strip():
            continue
        f = line.rstrip('\n').split('\t')
        if len(f) < 9 or f[2] != 'CDS':
            continue
        seqname, _, _, start, end, _, strand, phase, attr = f[:9]
        tx = parse_attr(attr, 'transcript_id') or parse_attr(attr, 'Parent')
        if tx is None:
            continue
        raw.setdefault(tx, []).append(
            (int(start), int(end), None if phase == '.' else int(phase)))
        if tx not in meta:
            meta[tx] = (seqname, strand,
                        parse_attr(attr, 'gene_id'),
                        parse_attr(attr, 'protein_id'))
        n += 1

    transcripts, index = {}, {}
    for tx, fl in raw.items():
        chrom, strand, gene_id, protein_id = meta[tx]
        fl.sort(key=lambda t: t[0], reverse=(strand == '-'))   # transcript order
        feats, cum = [], 0
        for s, e, ph in fl:
            feats.append({'start': s, 'end': e, 'phase': ph, 'cum': cum})
            cum += e - s + 1
        transcripts[tx] = {'chrom': chrom, 'strand': strand,
                           'gene_id': gene_id, 'protein_id': protein_id,
                           'feats': feats, 'cds_len': cum}
        chrom_idx = index.setdefault(chrom, {})
        for s, e, _ in fl:
            for b in range(s // BIN, e // BIN + 1):
                chrom_idx.setdefault(b, []).append((s, e, tx))
    return transcripts, index, n


def overlapping_transcripts(chrom, pos, index):
    chrom_idx = index.get(chrom)
    if chrom_idx is None:                       # try chr-prefix toggle
        alt = chrom[3:] if chrom.startswith('chr') else 'chr' + chrom
        chrom_idx = index.get(alt)
    if chrom_idx is None:
        return None, []                         # chromosome absent from GTF
    hits = [tx for (s, e, tx) in chrom_idx.get(pos // BIN, [])
            if s <= pos <= e]
    return True, sorted(set(hits))


# ----------------------------------------------------------------------------
# Mapping + edit (per transcript)
# ----------------------------------------------------------------------------
def genomic_to_cds_offset(pos, feats, strand):
    for ft in feats:
        if ft['start'] <= pos <= ft['end']:
            return ft['cum'] + (pos - ft['start'] if strand == '+'
                                else ft['end'] - pos)
    return None


def edit_and_translate(cds, tx_rec, pos, ref, alt, code=STANDARD_CODE):
    """Return dict with mutated protein + consequence for one transcript."""
    feats, strand = tx_rec['feats'], tx_rec['strand']
    offs = [genomic_to_cds_offset(p, feats, strand)
            for p in range(pos, pos + len(ref))]
    if any(o is None for o in offs):
        return {'consequence': 'splice/CDS-boundary spanning (skipped)',
                'mut_aa': None}
    lo, hi = min(offs), max(offs)
    if hi - lo + 1 != len(ref):
        return {'consequence': 'non-contiguous in CDS (skipped)', 'mut_aa': None}

    cds_ref = ref if strand == '+' else revcomp(ref)
    cds_alt = alt if strand == '+' else revcomp(alt)
    observed = cds[lo:hi + 1]
    warn = None
    if observed != cds_ref:
        warn = f"REF mismatch: CDS has '{observed}', variant implies '{cds_ref}'"

    orig_aa = translate(cds, code)
    mut_cds = cds[:lo] + cds_alt + cds[hi + 1:]
    mut_aa = translate(mut_cds, code)
    ci, d = lo // 3, len(alt) - len(ref)

    if d == 0:
        o = orig_aa[ci] if ci < len(orig_aa) else '?'
        m = mut_aa[ci] if ci < len(mut_aa) else '?'
        if o == m:
            cons = f"synonymous p.{o}{ci+1}="
        elif m == '*':
            cons = f"stop_gained p.{o}{ci+1}*"
        elif o == '*':
            cons = f"stop_lost p.*{ci+1}{m}"
        elif ci == 0 and o == 'M':
            cons = f"start_lost p.M1{m}"
        else:
            cons = f"missense p.{o}{ci+1}{m}"
    elif d % 3 == 0:
        cons = (f"inframe_{'deletion' if d < 0 else 'insertion'} "
                f"~codon {ci+1} ({d:+d} nt)")
    else:
        cons = f"frameshift from codon {ci+1} ({d:+d} nt)"

    return {'consequence': cons, 'mut_aa': mut_aa, 'orig_aa': orig_aa,
            'cds_offset': lo, 'codon': ci + 1, 'warn': warn}


# ----------------------------------------------------------------------------
def fold(seq, width=60):
    return '\n'.join(textwrap.wrap(seq, width)) if seq else ''


def annotate(chrom, pos, ref, alt, transcripts, index, cds_dict, aa_dict,
             restrict_tx=None):
    found, txs = overlapping_transcripts(chrom, pos, index)
    if found is None:
        return [{'tx': None, 'gene': None, 'consequence':
                 f'chromosome {chrom!r} not in GTF', 'mut_aa': None}]
    if not txs:
        return [{'tx': None, 'gene': None,
                 'consequence': 'no CDS overlap (intergenic/intron/UTR)',
                 'mut_aa': None}]
    out = []
    for tx in txs:
        if restrict_tx and tx != restrict_tx:
            continue
        rec = transcripts[tx]
        cds = lookup_seq(cds_dict, tx, rec.get('protein_id'))
        if cds is None:
            out.append({'tx': tx, 'gene': rec['gene_id'], 'mut_aa': None,
                        'consequence': 'CDS sequence not found in --cds FASTA'})
            continue
        # quiet length sanity
        len_warn = None
        if rec['cds_len'] not in (len(cds), len(cds) + 3, len(cds) - 3):
            len_warn = (f"GTF CDS len {rec['cds_len']} != FASTA len {len(cds)}")
        res = edit_and_translate(cds, rec, pos, ref, alt)
        # optional protein validation
        if aa_dict and res.get('orig_aa') is not None:
            given = lookup_seq(aa_dict, rec.get('protein_id'), tx)
            if given and res['orig_aa'].rstrip('*') != given.rstrip('*'):
                res['warn'] = ((res.get('warn') or '') +
                               ' | translated CDS != provided protein').strip()
        if len_warn:
            res['warn'] = ((res.get('warn') or '') + ' | ' + len_warn).strip(' |')
        res.update({'tx': tx, 'gene': rec['gene_id'], 'strand': rec['strand']})
        out.append(res)
    return out


def main():
    ap = argparse.ArgumentParser(
        description="Annotate variant(s) genome-wide and emit mutant proteins.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--variant', help="single CHROM_POS_REF_ALT (forward strand)")
    g.add_argument('--variants-file',
                   help="file of variants (CHROM_POS_REF_ALT, TSV, or VCF)")
    ap.add_argument('--gtf', required=True, help="whole-genome GTF (CDS)")
    ap.add_argument('--cds', required=True, help="genome-wide CDS FASTA")
    ap.add_argument('--aa', help="genome-wide protein FASTA (optional, validate)")
    ap.add_argument('--transcript-id', help="restrict to one transcript")
    ap.add_argument('--out', help="write mutant protein FASTA here")
    ap.add_argument('--tsv', help="write consequence table here")
    args = ap.parse_args()

    sys.stderr.write("Indexing GTF...\n")
    transcripts, index, n_cds = build_index(args.gtf)
    sys.stderr.write(f"  {len(transcripts)} transcripts, {n_cds} CDS features, "
                     f"{len(index)} sequences.\n")
    sys.stderr.write("Loading CDS FASTA...\n")
    cds_dict = read_fasta_dict(args.cds)
    aa_dict = read_fasta_dict(args.aa) if args.aa else None

    if args.variant:
        variants = [parse_variant(args.variant)]
    else:
        variants = list(iter_variants(args.variants_file))

    fasta_out = open(args.out, 'w') if args.out else None
    tsv_out = open(args.tsv, 'w') if args.tsv else None
    if tsv_out:
        tsv_out.write("variant\tgene_id\ttranscript_id\tstrand\t"
                      "consequence\tcds_offset\tcodon\twarning\n")

    for chrom, pos, ref, alt in variants:
        vid = f"{chrom}_{pos}_{ref}_{alt}"
        results = annotate(chrom, pos, ref, alt, transcripts, index,
                           cds_dict, aa_dict, args.transcript_id)
        for r in results:
            line = (f"{vid}\t{r.get('gene')}\t{r.get('tx')}\t"
                    f"{r.get('strand','')}\t{r['consequence']}\t"
                    f"{r.get('cds_offset','')}\t{r.get('codon','')}\t"
                    f"{r.get('warn') or ''}")
            if tsv_out:
                tsv_out.write(line + "\n")
            else:
                print("# " + line)
            if r.get('warn'):
                sys.stderr.write(f"WARNING {vid} {r.get('tx')}: {r['warn']}\n")
            if r.get('mut_aa'):
                header = (f">{vid}|{r.get('gene')}|{r.get('tx')}|"
                          f"{r['consequence'].split(' ')[0]}")
                rec = header + "\n" + fold(r['mut_aa'])
                if fasta_out:
                    fasta_out.write(rec + "\n")
                elif not tsv_out:
                    print(rec)

    if fasta_out:
        fasta_out.close()
        sys.stderr.write(f"Mutant proteins -> {args.out}\n")
    if tsv_out:
        tsv_out.close()
        sys.stderr.write(f"Consequence table -> {args.tsv}\n")


if __name__ == '__main__':
    main()
