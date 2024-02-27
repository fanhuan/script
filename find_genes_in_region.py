import sys
from collections import defaultdict, Counter

def parse_gff(gff_file):
    gene_annotations = defaultdict(list)
    gene_ID = defaultdict(list)
    with open(gff_file, 'r') as gff:
        for line in gff:
            if line.startswith("#") or line.strip() == "":
                continue
            parts = line.strip().split('\t')
            attributes = {attr.split('=')[0]: attr.split('=')[1] for attr in parts[8].split(';')}
            if parts[2] == 'gene':
                gene_ID[attributes['ID']].append(line.strip())
                gene_annotations[attributes['ID']].append(line.strip())
            elif 'Parent' in attributes:
                gene_annotations[attributes['Parent']].append(line.strip())
    dup_ID = []
    for key in gene_ID:
        if len(set(gene_ID[key])) > 1:
            dup_ID.append(key)
    for key in dup_ID:
        removed_value = gene_ID.pop(key, None)  # None is returned if 'b' is not found
        removed_value = gene_annotations.pop(key, None)  # None is returned if 'b' is not found
    return gene_ID, gene_annotations

def check_gene_contains_region(fasta_file, gff_file):
    gene_ID, gene_annotations = parse_gff(gff_file)

    with open(fasta_file, 'r') as fasta:
        for line in fasta:
            if line.startswith('>'):
                chr_name, region = line[1:].strip().split(':')
                start, end = map(int, region.split('-'))
                # Adjust for 0-based BED to 1-based GFF
                start += 1

                matched_genes = []
                for gene_id, annotations in gene_ID.items():
                    for annotation in annotations:
                        parts = annotation.split('\t')
                        gff_chr, gff_start, gff_end = parts[0], int(parts[3]), int(parts[4])
                        if chr_name == gff_chr and start >= gff_start and end <= gff_end:
                            matched_genes.append(gene_id)
                            sys.stderr.write(f"Gene {gene_id} contains region {chr_name}:{start-1}-{end}\n")

                # Only proceed if exactly one gene matches
                if len(set(matched_genes)) == 1:
                    for ann in gene_annotations[matched_genes[0]]:
                        print(ann)

if __name__ == "__main__":
    fasta_file = sys.argv[1]
    gff_file = sys.argv[2]
    check_gene_contains_region(fasta_file, gff_file)
