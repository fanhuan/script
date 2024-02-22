#!/usr/bin/env python3

import sys

def make_ids_unique(input_file):
    # Dictionary to keep track of IDs and their counts
    id_counts = {}

    with open(input_file, 'r') as infile:
        for line in infile:
            # Skip header lines or any line not containing an ID field
            if line.startswith('#') or 'ID=' not in line:
                print(line, end='')
                continue

            # Extract the ID value
            parts = line.split('\t')
            attributes = parts[8]  # Assuming attributes are in the 9th column
            id_part = [attr for attr in attributes.split(';') if 'ID=' in attr][0]
            original_id = id_part.split('=')[1]

            # Check if the ID already exists and generate a new unique ID
            if original_id in id_counts:
                # Increment the counter for this ID
                id_counts[original_id] += 1
                new_id = f"{original_id}.{id_counts[original_id]}"
            else:
                # Initialize the counter for this new ID
                id_counts[original_id] = 0
                new_id = original_id

            # Replace the original ID in the line with the new unique ID
            new_line = line.replace(f"ID={original_id}", f"ID={new_id}")

            print(new_line, end='')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: make_gff_unique.py <input_gff3_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    make_ids_unique(input_file)
