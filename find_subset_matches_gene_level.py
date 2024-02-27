import sys

def is_subset(start_a, end_a, start_b, end_b):
    """Check if coordinates from A are a subset of coordinates from B."""
    return start_b <= start_a and end_a <= end_b

def parse_gff_attributes(attributes_str):
    """Parse the GFF attribute string into a dictionary."""
    attributes = {}
    for attribute in attributes_str.split(';'):
        key, value = attribute.split('=')
        attributes[key] = value
    return attributes

def find_subset_matches_gene_level(a_gff_path, b_gff_path):
    """Find subset matches at gene level and output the ID from B.gff."""
    # Parse B.gff to create a list of tuples containing coordinates and IDs for 'gene' entries
    b_genes = []
    with open(b_gff_path, 'r') as b_gff:
        for line in b_gff:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split('\t')
            if parts[2] == 'gene':  # Only consider entries that are genes
                attributes = parse_gff_attributes(parts[8])
                if 'ID' in attributes:
                    b_genes.append((parts[0], int(parts[3]), int(parts[4]), attributes['ID']))

    # Process A.gff and attempt to find subset matches in B.gff
    with open(a_gff_path, 'r') as a_gff:
        for line in a_gff:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split('\t')
            start_a, end_a = int(parts[3]), int(parts[4])
            
            for seqid_b, start_b, end_b, id_b in b_genes:
                if parts[0] == seqid_b and is_subset(start_a, end_a, start_b, end_b):
                    print(id_b)
                    break  # Stop searching once a match is found for this line

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python find_subset_matches_gene_level.py <A.gff> <B.gff>")
        sys.exit(1)
    find_subset_matches_gene_level(sys.argv[1], sys.argv[2])
