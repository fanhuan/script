#!/usr/bin/env python3
"""Find transcripts whose five_prime_UTR sits AT or DOWNSTREAM of the start
codon (i.e. inside the CDS) -- the SnpEff-breaking signature. Also flag whether
the 5' CDS that SnpEff would drop is a non-multiple-of-3 (=> frameshift =>
internal stops)."""
import sys
from collections import defaultdict

gtf = sys.argv[1]
tx = defaultdict(lambda: {'strand': None, 'start_codon': None,
                          'futr': [], 'cds': []})

def attr(a, key):
    for c in a.split(';'):
        c = c.strip()
        if c.startswith(key):
            return c[len(key):].strip().strip('"').strip()
    return None

for line in open(gtf):
    if line.startswith('#') or not line.strip():
        continue
    f = line.rstrip('\n').split('\t')
    if len(f) < 9:
        continue
    feat, s, e, strand = f[2], int(f[3]), int(f[4]), f[6]
    t = attr(f[8], 'transcript_id')
    if t is None:
        continue
    r = tx[t]
    r['strand'] = strand
    if feat == 'start_codon':
        r['start_codon'] = (s, e)
    elif feat == 'five_prime_UTR':
        r['futr'].append((s, e))
    elif feat == 'CDS':
        r['cds'].append((s, e))

n_tx = len(tx)
n_with_futr = 0
bad = []          # 5'UTR downstream of start codon
frameshift = 0    # of the bad ones, dropped 5' CDS not multiple of 3

for t, r in tx.items():
    if not r['futr']:
        continue
    n_with_futr += 1
    sc = r['start_codon']
    if sc is None:
        continue
    is_bad = False
    if r['strand'] == '+':
        # legit 5'UTR must end strictly before the start codon start
        is_bad = any(us >= sc[0] for (us, ue) in r['futr'])
    else:
        is_bad = any(ue <= sc[1] for (us, ue) in r['futr'])
    if not is_bad:
        continue
    bad.append(t)
    # estimate dropped 5' CDS length = CDS bases that fall 5' of the
    # furthest-downstream 5'UTR boundary
    if r['strand'] == '+':
        cutoff = max(ue for (us, ue) in r['futr'])
        dropped = sum(min(e, cutoff) - s + 1 for (s, e) in r['cds']
                      if s <= cutoff)
    else:
        cutoff = min(us for (us, ue) in r['futr'])
        dropped = sum(e - max(s, cutoff) + 1 for (s, e) in r['cds']
                      if e >= cutoff)
    if dropped % 3 != 0:
        frameshift += 1

print(f"total transcripts:               {n_tx}")
print(f"transcripts with a 5'UTR:        {n_with_futr}")
print(f"5'UTR misplaced into CDS (BAD):   {len(bad)}"
      f"   ({100*len(bad)/n_tx:.1f}% of all tx)")
print(f"  ...of those, frameshift (worst): {frameshift}")
print()
print("examples (first 15 bad transcripts):")
for t in bad[:15]:
    print("  ", t)
