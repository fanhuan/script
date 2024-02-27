import sys

# Assuming the script is called with: python script.py A.gff B.gff min_overlap_percentage

# File paths and minimum overlap percentage
a_gff_path = sys.argv[1]
b_gff_path = sys.argv[2]
min_overlap_percentage = float(sys.argv[3])  # Minimum overlap percentage as a float

# Function to calculate overlap percentage
def calculate_overlap(start1, end1, start2, end2):
    overlap = max(0, min(end1, end2) - max(start1, start2))
    length1 = end1 - start1
    return (overlap / length1) * 100 if length1 else 0

# Parse B.gff to create a list of features with their coordinates and IDs
b_features = []
with open(b_gff_path, 'r') as b_gff:
    for line in b_gff:
        if line.startswith('#') or line.strip() == '':
            continue
        parts = line.strip().split('\t')
        seqid, _, feature_type, start, end, _, strand, _, attributes = parts
        attr_dict = {attr.split('=')[0]: attr.split('=')[1] for attr in attributes.split(';') if '=' in attr}
        if 'ID' in attr_dict:
            b_features.append((seqid, int(start), int(end), strand, feature_type, attr_dict['ID']))

# Process A.gff and attempt to find matches in B.gff based on exact or minimum overlap criteria
with open(a_gff_path, 'r') as a_gff:
    for line in a_gff:
        if line.startswith('#') or line.strip() == '':
            print(line, end='')
            continue
        parts = line.strip().split('\t')
        seqid, _, feature_type, start, end, _, strand, _, attributes = parts
        start, end = int(start), int(end)
        
        # Attempt to find an exact match first
        match_id = None
        for b_seqid, b_start, b_end, b_strand, b_feature_type, b_id in b_features:
            if seqid == b_seqid and strand == b_strand and feature_type == b_feature_type:
                if start == b_start and end == b_end:
                    match_id = b_id
                    break
                elif calculate_overlap(start, end, b_start, b_end) >= min_overlap_percentage:
                    match_id = b_id
                    break
        
        # Replace target_ID with the found ID, or modify as needed
        if match_id:
            new_attributes = ';'.join([f"ID={match_id}" if attr.startswith('target_ID') else attr for attr in attributes.split(';')])
            parts[8] = new_attributes
        print('\t'.join(parts))
