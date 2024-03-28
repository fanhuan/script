import sys
from collections import defaultdict, Counter

def extract_features_by_id(gff_file, target_id):
    # Store entries by ID and Parent ID for quick lookup
    entries_by_id = {}
    entries_by_parent = {}

    # Read GFF file
    with open(gff_file, 'r') as gff_file:
        for line in gff_file:
            if line.startswith('#') or line.strip() == '':
                continue  # Skip comments and empty lines
            
            parts = line.strip().split('\t')
            attributes = parts[8]
            attr_dict = {attr.split('=')[0]: attr.split('=')[1] for attr in attributes.split(';') if '=' in attr}
            
            # Store the entry by its ID (if available)
            if 'ID' in attr_dict:
                entries_by_id[attr_dict['ID']] = line.strip()
            
            # Map entry to its parent ID (if available)
            if 'Parent' in attr_dict:
                parent_id = attr_dict['Parent']
                if parent_id not in entries_by_parent:
                    entries_by_parent[parent_id] = []
                entries_by_parent[parent_id].append(line.strip())
    
    def find_nested_entries(entry_id, collected_entries):
        """Recursively collect nested entries."""
        if entry_id in entries_by_parent:
            for nested_entry in entries_by_parent[entry_id]:
                collected_entries.append(nested_entry)
                nested_id = nested_entry.split('\t')[8].split(';')[0].split('=')[1]
                find_nested_entries(nested_id, collected_entries)
    
    # Start with the target ID and collect all related entries
    collected_entries = []
    if target_id in entries_by_id:
        collected_entries.append(entries_by_id[target_id])
        find_nested_entries(target_id, collected_entries)
    
    return collected_entries


def parse_gff(gff_file):
    gene_ID = defaultdict(list)
    with open(gff_file, 'r') as gff:
        for line in gff:
            if line.startswith("#") or line.strip() == "":
                continue
            parts = line.strip().split('\t')
            attributes = {attr.split('=')[0]: attr.split('=')[1] for attr in parts[8].split(';')}
            if parts[2] == 'gene':
                gene_ID[attributes['ID']].append(line.strip())

    dup_ID = []
    for key in gene_ID:
        if len(set(gene_ID[key])) > 1:
            dup_ID.append(key)
    for key in dup_ID:
        removed_value = gene_ID.pop(key, None)  # None is returned if 'b' is not found
    return gene_ID

def check_gene_contains_region(fasta_file, gff_file):
    gene_ID = parse_gff(gff_file)

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
                    collected_entries = extract_features_by_id(gff_file, matched_genes[0])
                    for entry in collected_entries:
                        print(entry)

if __name__ == "__main__":
    fasta_file = sys.argv[1]
    gff_file = sys.argv[2]
    check_gene_contains_region(fasta_file, gff_file)

