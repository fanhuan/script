#!/usr/bin/env python3
import argparse
import pysam

def parse_args():
    p = argparse.ArgumentParser(
        description="Remap BAM coordinates to one concatenated contig with fixed N-spacers between chromosomes."
    )
    p.add_argument("in_bam", help="Input BAM (name- or coordinate-sorted; index not required).")
    p.add_argument("out_bam", help="Output BAM on single concatenated contig.")
    p.add_argument("--contig-name", default="concat",
                   help="Name for the concatenated contig (default: concat).")
    p.add_argument("--spacer", type=int, default=500,
                   help="Spacer size in bp inserted between chromosomes (default: 500).")
    p.add_argument("--keep-chr-order-from", choices=["header","alpha"], default="header",
                   help="Use chromosome order from BAM header (default) or alphabetical.")
    p.add_argument("--keep-unmapped", action="store_true",
                   help="Write unmapped reads through unchanged (default: drop them).")
    return p.parse_args()

def build_offsets(in_bam, order_mode="header", spacer=500):
    # Collect SQs
    sqs = [(sq["SN"], sq["LN"]) for sq in in_bam.header.get("SQ", [])]
    if not sqs:
        raise RuntimeError("Input BAM header has no @SQ lines; cannot compute offsets.")
    if order_mode == "alpha":
        sqs.sort(key=lambda x: x[0])

    offsets = {}
    pads = []  # list of (pad_start, pad_end) intervals in the final contig (0-based, end-exclusive)
    running = 0
    for i, (name, ln) in enumerate(sqs):
        offsets[name] = running
        running += ln
        # Add spacer after each chrom except the last
        if i != len(sqs) - 1 and spacer > 0:
            pads.append((running, running + spacer))
            running += spacer

    total_len = running
    chrom_order = [n for n, _ in sqs]
    chrom_lengths = {n: ln for n, ln in sqs}
    return offsets, total_len, chrom_order, chrom_lengths, pads

def rewrite_sa_tag(sa, offsets, new_rname):
    # SA:Z:rname,pos,strand,cigar,mapQ,NM;...
    parts = sa.rstrip(";").split(";")
    out_parts = []
    for entry in parts:
        if not entry:
            continue
        fields = entry.split(",")
        if len(fields) < 6:
            out_parts.append(entry)
            continue
        rname, pos, strand, cigar, mapq, nm = fields[:6]
        try:
            pos_i = int(pos)
        except ValueError:
            out_parts.append(entry); continue
        off = offsets.get(rname)
        if off is not None:
            rname = new_rname
            pos_i = off + (pos_i - 1)  # SA:Z pos is 1-based
            fields[:6] = [rname, str(pos_i + 1), strand, cigar, mapq, nm]  # keep 1-based
        out_parts.append(",".join(fields))
    return ";".join(out_parts) + ";"

def main():
    args = parse_args()
    in_bam = pysam.AlignmentFile(args.in_bam, "rb")

    offsets, total_len, chrom_order, chrom_lengths, pads = build_offsets(
        in_bam, args.keep_chr_order_from, args.spacer
    )

    # Build new header: single @SQ, copy the rest
    new_header = in_bam.header.to_dict()
    new_header["SQ"] = [{"SN": args.contig_name, "LN": total_len}]
    # Record composition in @CO (helpful for downstream sanity checks)
    comp = []
    for i, cname in enumerate(chrom_order):
        comp.append(f"{cname}:len={chrom_lengths[cname]},off={offsets[cname]}")
        if i != len(chrom_order) - 1 and args.spacer > 0:
            s, e = pads[i]
            comp.append(f"[PAD {args.spacer}bp @ {s}-{e})")
    new_header.setdefault("CO", []).append(
        "Concatenated contig {} built from: {}".format(args.contig_name, " | ".join(comp))
    )

    out_bam = pysam.AlignmentFile(args.out_bam, "wb", header=new_header)
    new_tid = out_bam.get_tid(args.contig_name)

    # Iterate records regardless of sorting/index
    for rec in in_bam.fetch(until_eof=True):

        # Optionally drop unmapped to keep output tidy (default behavior)
        if rec.is_unmapped:
            if args.keep_unmapped:
                out_bam.write(rec)
            continue

        old_tid = rec.reference_id
        old_rname = in_bam.get_reference_name(old_tid)
        off = offsets.get(old_rname)
        if off is None:
            # Unknown reference: pass through unchanged (rare)
            out_bam.write(rec)
            continue

        # Update primary reference
        rec.reference_id = new_tid
        # pysam is 0-based; add offset
        rec.reference_start = off + rec.reference_start

        # Mate handling
        orig_mate_same_chrom = False
        if not rec.mate_is_unmapped:
            mate_rname = rec.next_reference_name
            mate_off = offsets.get(mate_rname)
            if mate_off is not None:
                rec.next_reference_id = new_tid
                rec.next_reference_start = mate_off + rec.next_reference_start
                if mate_rname == old_rname:
                    orig_mate_same_chrom = True
            # else: leave as-is (unexpected)

        # TLEN policy: keep original if mates were on same original chrom; else set 0
        if rec.mate_is_unmapped:
            rec.template_length = 0
        else:
            if not orig_mate_same_chrom:
                rec.template_length = 0
            # else: keep original TLEN (distance preserved under constant offset)

        # Rewrite SA:Z if present
        if rec.has_tag("SA"):
            sa_new = rewrite_sa_tag(rec.get_tag("SA"), offsets, args.contig_name)
            rec.set_tag("SA", sa_new, value_type="Z")

        # Write out
        out_bam.write(rec)

    in_bam.close()
    out_bam.close()

    # Done
    # (Sorting/indexing left to the user to keep this script lean.)

if __name__ == "__main__":
    main()

