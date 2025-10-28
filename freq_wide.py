#!/usr/bin/env python3
"""
PLINK FST Filter and Frequency Data Processor

This script processes large PLINK --fst and --freq output files to:
1. Filter SNPs with FST > 0.25 (or user-specified threshold)
2. Convert frequency data from long to wide format with MAF values

Usage:
    python process_plink.py --fst fst_file.fst --freq freq_file.frq --snps snp_list.txt --output output.tsv --fst-threshold 0.25

Requirements:
    pandas
"""

import pandas as pd
import argparse
import sys
from pathlib import Path

def read_snp_list(snp_file):
    """Read SNP list from file, one SNP per line."""
    try:
        with open(snp_file, 'r') as f:
            snps = [line.strip() for line in f if line.strip()]
        print(f"Loaded {len(snps)} SNPs from {snp_file}")
        return set(snps)
    except FileNotFoundError:
        print(f"Error: SNP file {snp_file} not found")
        sys.exit(1)

def filter_fst_snps(fst_file, threshold=0.25):
    """
    Filter SNPs from FST file based on FST threshold.
    Assumes FST file has columns: CHR, SNP, FST
    Returns set of SNP names that pass the threshold.
    """
    try:
        print(f"Reading FST file: {fst_file}")
        # Read FST file in chunks to handle large files
        high_fst_snps = set()
        chunk_size = 10000
        
        for chunk in pd.read_csv(fst_file, sep='\t', chunksize=chunk_size):
            # Filter SNPs with FST > threshold
            filtered_chunk = chunk[chunk['FST'] > threshold]
            high_fst_snps.update(filtered_chunk['SNP'].tolist())
            
        print(f"Found {len(high_fst_snps)} SNPs with FST > {threshold}")
        return high_fst_snps
        
    except FileNotFoundError:
        print(f"Error: FST file {fst_file} not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading FST file: {e}")
        sys.exit(1)

def process_frequency_data(freq_file, selected_snps, output_file):
    """
    Process frequency data: filter by selected SNPs and pivot to wide format.
    Input format: CHR, SNP, CLST, A1, A2, MAF, MAC, NCHROBS
    Output format: SNP, cluster1_MAF, cluster2_MAF, ...
    """
    try:
        print(f"Processing frequency file: {freq_file}")
        
        # Process in chunks for memory efficiency
        chunk_size = 50000
        processed_chunks = []
        
        for chunk in pd.read_csv(freq_file, sep='\t', chunksize=chunk_size):
            # Filter for selected SNPs only
            filtered_chunk = chunk[chunk['SNP'].isin(selected_snps)]
            
            if not filtered_chunk.empty:
                # Keep only necessary columns
                filtered_chunk = filtered_chunk[['SNP', 'CLST', 'MAF']].copy()
                processed_chunks.append(filtered_chunk)
        
        if not processed_chunks:
            print("No data found for selected SNPs")
            return
            
        # Combine all chunks
        freq_data = pd.concat(processed_chunks, ignore_index=True)
        print(f"Loaded {len(freq_data)} frequency records for {freq_data['SNP'].nunique()} SNPs")
        
        # Pivot to wide format
        print("Converting to wide format...")
        wide_data = freq_data.pivot(index='SNP', columns='CLST', values='MAF')
        
        # Reset index to make SNP a column
        wide_data = wide_data.reset_index()
        
        # Fill NaN values with 0 (assuming missing = 0 frequency)
        wide_data = wide_data.fillna(0)
        
        # Sort by SNP name for consistent output
        wide_data = wide_data.sort_values('SNP')
        
        # Save to file
        wide_data.to_csv(output_file, sep='\t', index=False, float_format='%.5f')
        print(f"Output saved to: {output_file}")
        print(f"Final dataset: {len(wide_data)} SNPs × {len(wide_data.columns)-1} clusters")
        
        # Print summary statistics
        print("\nSummary:")
        print(f"- Number of SNPs: {len(wide_data)}")
        print(f"- Number of clusters: {len(wide_data.columns)-1}")
        print(f"- Cluster names: {', '.join(wide_data.columns[1:])}")
        
        return wide_data
        
    except FileNotFoundError:
        print(f"Error: Frequency file {freq_file} not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing frequency data: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Process PLINK FST and frequency files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # FST filtering only (no SNP list needed)
    python process_plink.py --fst data.fst --freq data.frq --output results.tsv
    
    # Custom FST threshold
    python process_plink.py --fst data.fst --freq data.frq --output results.tsv --fst-threshold 0.15
    
    # Use specific SNP list without FST filtering
    python process_plink.py --freq data.frq --snps snp_list.txt --output results.tsv --no-fst-filter
    
    # FST filtering + intersect with SNP list (if you want both filters)
    python process_plink.py --fst data.fst --freq data.frq --snps snp_list.txt --output results.tsv
        """
    )
    
    parser.add_argument('--fst', type=str, help='FST file from plink --fst')
    parser.add_argument('--freq', type=str, required=True, help='Frequency file from plink --freq')
    parser.add_argument('--snps', type=str, help='File with SNP names (one per line). Required if using --no-fst-filter')
    parser.add_argument('--output', type=str, required=True, help='Output file name')
    parser.add_argument('--fst-threshold', type=float, default=0.25, 
                       help='FST threshold for filtering (default: 0.25)')
    parser.add_argument('--no-fst-filter', action='store_true',
                       help='Skip FST filtering, use all SNPs from SNP list')
    
    args = parser.parse_args()
    
    # Validate input files
    if not Path(args.freq).exists():
        print(f"Error: Frequency file {args.freq} does not exist")
        sys.exit(1)
    
    if args.no_fst_filter and not args.snps:
        print("Error: --snps file is required when using --no-fst-filter")
        sys.exit(1)
    
    if not args.no_fst_filter and not args.fst:
        print("Error: Either provide --fst file or use --no-fst-filter with --snps")
        sys.exit(1)
    
    if args.fst and not Path(args.fst).exists():
        print(f"Error: FST file {args.fst} does not exist")
        sys.exit(1)
        
    if args.snps and not Path(args.snps).exists():
        print(f"Error: SNP file {args.snps} does not exist")
        sys.exit(1)
    
    # Read SNP list if provided
    snp_list = read_snp_list(args.snps) if args.snps else None
    
    # Filter by FST if requested
    if not args.no_fst_filter:
        high_fst_snps = filter_fst_snps(args.fst, args.fst_threshold)
        if snp_list:
            # Intersect with SNP list if both are provided
            selected_snps = snp_list.intersection(high_fst_snps)
            print(f"Selected {len(selected_snps)} SNPs (intersection of SNP list and FST > {args.fst_threshold})")
        else:
            # Use only FST-filtered SNPs
            selected_snps = high_fst_snps
            print(f"Selected {len(selected_snps)} SNPs with FST > {args.fst_threshold}")
    else:
        selected_snps = snp_list
        print(f"Using all {len(selected_snps)} SNPs from SNP list (no FST filtering)")
    
    if not selected_snps:
        print("No SNPs selected. Check your FST threshold and SNP list.")
        sys.exit(1)
    
    # Process frequency data
    process_frequency_data(args.freq, selected_snps, args.output)

if __name__ == "__main__":
    main()
