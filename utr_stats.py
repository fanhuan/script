#!/usr/bin/env python3
"""Summarise UTR annotation in one or more GTFs produced by stringtie2utr.py.

For each file reports: #transcripts, #with 5'UTR, #with 3'UTR, total UTR
feature counts, total UTR bp, the longest single UTR, how many UTRs exceed
5 kb (to show BRAKER4's max_utr_extension clipping), and how many transcripts
have a UTR misplaced *inside* the CDS (the SnpEff-breaking bug)."""
import sys
from collections import defaultdict


def stats(path):
    tx = set()
    has5 = set()
    has3 = set()
    n5 = n3 = bp5 = bp3 = 0
    longest = 0
    over5k = 0
    # per-transcript coding span + utrs, to count misplaced-in-CDS
    cds = defaultdict(lambda: [None, None])   # tx -> [min_start, max_end]
    utrs = defaultdict(list)                   # tx -> [(start,end), ...]

    def attr(a):
        for c in a.split(';'):
            c = c.strip()
            if c.startswith('transcript_id'):
                return c.split('"')[1] if '"' in c else c.split()[-1]
        return None

    with open(path) as fh:
        for line in fh:
            if line.startswith('#') or not line.strip():
                continue
            f = line.rstrip('\n').split('\t')
            if len(f) < 9:
                continue
            feat, s, e = f[2], int(f[3]), int(f[4])
            t = attr(f[8])
            if t is None:
                continue
            if feat == 'transcript':
                tx.add(t)
            elif feat == 'CDS':
                tx.add(t)
                lo, hi = cds[t]
                cds[t][0] = s if lo is None else min(lo, s)
                cds[t][1] = e if hi is None else max(hi, e)
            elif feat in ('five_prime_UTR', 'three_prime_UTR'):
                tx.add(t)
                length = e - s + 1
                longest = max(longest, length)
                if length > 5000:
                    over5k += 1
                utrs[t].append((s, e))
                if feat == 'five_prime_UTR':
                    has5.add(t); n5 += 1; bp5 += length
                else:
                    has3.add(t); n3 += 1; bp3 += length

    bad = 0
    for t, uu in utrs.items():
        lo, hi = cds.get(t, [None, None])
        if lo is None:
            continue
        if any(us <= hi and ue >= lo for (us, ue) in uu):
            bad += 1

    return {
        'tx': len(tx), 'has5': len(has5), 'has3': len(has3),
        'n5': n5, 'n3': n3, 'bp5': bp5, 'bp3': bp3,
        'longest': longest, 'over5k': over5k, 'bad_in_cds': bad,
    }


labels = ['transcripts', "tx w/ 5'UTR", "tx w/ 3'UTR",
          "5'UTR feats", "3'UTR feats", "5'UTR bp", "3'UTR bp",
          'longest UTR', 'UTR >5kb', 'UTR-in-CDS (BUG)']
keys = ['tx', 'has5', 'has3', 'n5', 'n3', 'bp5', 'bp3',
        'longest', 'over5k', 'bad_in_cds']

cols = [(p.split('/')[-1], stats(p)) for p in sys.argv[1:]]
w = max(len(l) for l in labels) + 1
hdr = ' '.join(f'{name[:18]:>18}' for name, _ in cols)
print(f"{'metric':<{w}} {hdr}")
for lab, k in zip(labels, keys):
    row = ' '.join(f'{s[k]:>18,}' for _, s in cols)
    print(f"{lab:<{w}} {row}")
