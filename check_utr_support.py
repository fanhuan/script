#!/usr/bin/env python3
"""Quantify RNA-seq support for a transcript's 5'UTR call.

For each gene it region-merges ALL bams in --bamdir over the locus (fast,
index-based), then compares mean read depth over the 5'UTR vs the first coding
exon. A real UTR extension shows continuous coverage (UTR depth ~ CDS depth); a
matching artifact shows a near-empty UTR or a separate upstream peak.

Usage:
  check_utr_support.py --gtf braker.utr.b4fixed.gtf --bamdir /path/to/bams g17412 g4605 g28099
"""
import argparse, glob, os, re, subprocess, sys, tempfile


def gene_zones(gtf, gene):
    """Return (chrom, strand, (utr_lo,utr_hi), (cds_lo,cds_hi)) where cds is the
    first coding exon (translation start side)."""
    pat = re.compile(r'transcript_id "%s\.' % re.escape(gene))
    chrom = strand = None
    utr_lo = utr_hi = None
    cds = []
    for line in open(gtf):
        f = line.rstrip('\n').split('\t')
        if len(f) < 9 or not pat.search(f[8]):
            continue
        s, e = int(f[3]), int(f[4])
        if f[2] == 'five_prime_UTR':
            chrom, strand = f[0], f[6]
            utr_lo = s if utr_lo is None else min(utr_lo, s)
            utr_hi = e if utr_hi is None else max(utr_hi, e)
        elif f[2] == 'CDS':
            chrom, strand = f[0], f[6]
            cds.append((s, e))
    if not cds:
        return None
    first = min(cds, key=lambda x: x[0]) if strand == '+' else max(cds, key=lambda x: x[1])
    return chrom, strand, (utr_lo, utr_hi), first


def mean_depth(bam, chrom, lo, hi):
    if lo is None:
        return float('nan')
    out = subprocess.run(['samtools', 'depth', '-a', '-r', f'{chrom}:{lo}-{hi}', bam],
                         capture_output=True, text=True).stdout
    tot = n = 0
    for ln in out.splitlines():
        tot += int(ln.split('\t')[2]); n += 1
    return tot / n if n else 0.0


def spliced_reads(bam, chrom, lo, hi):
    out = subprocess.run(['samtools', 'view', bam, f'{chrom}:{lo}-{hi}'],
                         capture_output=True, text=True).stdout
    return sum(1 for ln in out.splitlines() if 'N' in ln.split('\t')[5])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gtf', required=True)
    ap.add_argument('--bamdir', required=True)
    ap.add_argument('--pattern', default='*.bam')
    ap.add_argument('genes', nargs='+')
    a = ap.parse_args()

    bams = sorted(glob.glob(os.path.join(a.bamdir, a.pattern)))
    if not bams:
        sys.exit(f"no bams matched {a.bamdir}/{a.pattern}")
    sys.stderr.write(f"{len(bams)} bams\n")

    print(f"{'gene':<10}{'5UTR depth':>12}{'CDS depth':>12}{'UTR/CDS':>9}"
          f"{'upstream3kb':>13}{'spliced':>9}  verdict")
    for g in a.genes:
        z = gene_zones(a.gtf, g)
        if not z:
            print(f"{g:<10}  no CDS/UTR found"); continue
        chrom, strand, (ulo, uhi), (clo, chi) = z
        lo = min(x for x in (ulo, clo) if x is not None) - 3000
        hi = max(uhi or 0, chi) + 1000
        with tempfile.NamedTemporaryFile(suffix='.bam', delete=False) as tf:
            mb = tf.name
        subprocess.run(['samtools', 'merge', '-f', '-R', f'{chrom}:{lo}-{hi}', mb] + bams,
                       capture_output=True)
        subprocess.run(['samtools', 'index', mb], capture_output=True)

        ud = mean_depth(mb, chrom, ulo, uhi)
        cd = mean_depth(mb, chrom, clo, chi)
        # upstream-of-UTR window (where a neighbor/read-through would show up)
        if strand == '+':
            up = mean_depth(mb, chrom, max(1, ulo - 3000), ulo - 1)
        else:
            up = mean_depth(mb, chrom, uhi + 1, uhi + 3000)
        spl = spliced_reads(mb, chrom, ulo, uhi)
        ratio = ud / cd if cd else float('nan')
        verdict = ('continuous (looks real)' if ratio >= 0.5 else
                   'PARTIAL — inspect' if ratio >= 0.2 else
                   'WEAK UTR coverage — likely artifact')
        print(f"{g:<10}{ud:>12.1f}{cd:>12.1f}{ratio:>9.2f}{up:>13.1f}{spl:>9}  {verdict}")
        os.unlink(mb); os.unlink(mb + '.bai')


if __name__ == '__main__':
    main()
