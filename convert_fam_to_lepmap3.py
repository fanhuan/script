import pandas as pd
import argparse

def plink_fam_to_lepmap3(fam_file, output_file):
    """
    Convert a PLINK .fam file to a Lep-MAP3 pedigree file.
    
    Args:
        fam_file (str): Path to PLINK .fam file.
        output_file (str): Path to save Lep-MAP3 pedigree file.
    """
    try:
        # Load PLINK .fam file
        fam = pd.read_csv(fam_file, sep='\s+', header=None, 
                          names=["FID", "IID", "FatherID", "MotherID", "Sex", "Pheno"])
        
        
        # Create Lep-MAP3 structure (6 rows)
        rows = [
            ["CHR", "POS"] + ["family_name"] * len(fam["IID"]),  # Row 1: Header
            ["CHR", "POS"] + fam["IID"].tolist(),                # Row 2: Individual IDs
            ["CHR", "POS"] + ["0" if pd.isna(id_) else id_ for id_ in fam["FatherID"]],  # Row 3: Fathers
            ["CHR", "POS"] + ["0" if pd.isna(id_) else id_ for id_ in fam["MotherID"]],  # Row 4: Mothers
            ["CHR", "POS"] + [str(sex) if sex != 0 else "0" for sex in fam["Sex"]],      # Row 5: Sex
            ["CHR", "POS"] + ["0"] * len(fam["IID"])                                     # Row 6: Phenotypes
        ]
        
        # Write to output file
        with open(output_file, 'w') as f:
            for row in rows:
                f.write("\t".join(row) + "\n")
        print(f"Success! Lep-MAP3 pedigree saved to: {output_file}")

    except Exception as e:
        print(f"Error: {e}")
        exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Convert PLINK .fam file to Lep-MAP3 pedigree format."
    )
    parser.add_argument("input_fam", help="Path to PLINK .fam file")
    parser.add_argument("output_pedigree", help="Path to output Lep-MAP3 pedigree file")
    args = parser.parse_args()
    
    plink_fam_to_lepmap3(args.input_fam, args.output_pedigree)

if __name__ == "__main__":
    main()
