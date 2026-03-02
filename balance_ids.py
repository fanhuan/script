#!/usr/bin/env python3
import argparse
import random
from collections import defaultdict
from pathlib import Path

parser = argparse.ArgumentParser(
    description="Downsample each population in a .ids file to the smallest population size.")
parser.add_argument("ids", help="Input .ids file (3-column: name pop include)")
parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
parser.add_argument("--max", type=int, default=None, metavar="N",
                    help="Maximum individuals to keep per population (default: smallest population size)")
parser.add_argument("--keep-indi", default=None, metavar="FILE",
                    help="File with individual names to prioritise (one per line); "
                         "remaining slots up to target are filled randomly")
parser.add_argument("--ignore-pop", default=None, metavar="FILE",
                    help="File with population names to exclude entirely (one per line)")
args = parser.parse_args()

if args.seed is not None:
    random.seed(args.seed)

inpath = Path(args.ids)
outpath = inpath.with_suffix("").with_suffix("") if inpath.suffix == ".ids" else inpath
outpath = Path(str(inpath).removesuffix(".ids") + ".balanced.ids")

rows = []
with open(inpath) as f:
    for line in f:
        parts = line.split()
        if not parts:
            continue
        name = parts[0]
        pop  = parts[1] if len(parts) >= 2 else "unknown"
        inc  = int(parts[2]) if len(parts) >= 3 else 1
        rows.append([name, pop, inc])

# load ignore list if provided
ignored_pops = set()
if args.ignore_pop:
    with open(args.ignore_pop) as f:
        ignored_pops = {line.strip() for line in f if line.strip()}
    unknown_pops = ignored_pops - {row[1] for row in rows}
    if unknown_pops:
        print(f"WARNING: {len(unknown_pops)} population(s) in --ignore-pop not found in ids file: {', '.join(sorted(unknown_pops))}")

# group indices by population (only currently included individuals, excluding ignored pops)
pop_indices = defaultdict(list)
for i, (name, pop, inc) in enumerate(rows):
    if inc == 1 and pop not in ignored_pops:
        pop_indices[pop].append(i)

min_n = min(len(v) for v in pop_indices.values())
target_n = args.max if args.max is not None else min_n

print(f"Population sizes:")
for pop, idx in sorted(pop_indices.items()):
    print(f"  {pop}: {len(idx)}")
if ignored_pops:
    print(f"Ignored populations (set to 0): {', '.join(sorted(ignored_pops))}")
print(f"Keeping up to {target_n} per population")

# load priority keep list if provided
priority = set()
if args.keep_indi:
    with open(args.keep_indi) as f:
        priority = {line.strip() for line in f if line.strip()}
    unknown = priority - {row[0] for row in rows}
    if unknown:
        print(f"WARNING: {len(unknown)} name(s) in --keep-indi not found in ids file: {', '.join(sorted(unknown))}")
    ignored_indi = {row[0] for row in rows if row[1] in ignored_pops}
    skipped = priority & ignored_indi
    if skipped:
        print(f"WARNING: {len(skipped)} name(s) in --keep-indi belong to ignored populations and will be excluded: {', '.join(sorted(skipped))}")
    priority -= ignored_indi

# mark all currently-included rows as excluded, then re-include the kept sample
for i, row in enumerate(rows):
    if row[2] == 1:
        rows[i][2] = 0

for pop, idx in pop_indices.items():
    must   = [i for i in idx if rows[i][0] in priority]
    others = [i for i in idx if rows[i][0] not in priority]

    keep_n = min(len(idx), target_n)
    # always include priority individuals (even if they exceed target_n)
    chosen = must[:]
    remaining = keep_n - len(chosen)
    if remaining > 0:
        chosen += random.sample(others, min(len(others), remaining))

    for i in chosen:
        rows[i][2] = 1

with open(outpath, "w") as f:
    for name, pop, inc in rows:
        f.write(f"{name} {pop} {inc}\n")

print(f"Written to {outpath}")
