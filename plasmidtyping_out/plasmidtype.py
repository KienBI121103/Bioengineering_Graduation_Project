#!/bin/bash/env python3
import pandas as pd
import os
import glob
import sys

def process_plasmid_file(file_path):
    """
    Process a single plasmid typing results file
    """
    try:
        print(f"Processing: {file_path}")
        
        # Define expected headers
        headers = ['qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen', 
                  'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore']
        
        # Try to read the file directly with proper headers
        try:
            # First try: assume it's a proper tab-separated file with headers
            plasmidtype = pd.read_csv(file_path, sep='\t', header=0)
            
            # If it doesn't have the right number of columns, try without headers
            if len(plasmidtype.columns) != len(headers):
                plasmidtype = pd.read_csv(file_path, sep='\t', header=None, names=headers)
                
        except:
            # Second try: read as text and parse manually
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            # Remove empty lines and strip whitespace
            lines = [line.strip() for line in lines if line.strip()]
            
            # Split each line by tabs or spaces
            rows = []
            for line in lines:
                # Try tab separation first, then space separation
                if '\t' in line:
                    row = line.split('\t')
                else:
                    row = line.split()
                
                # Only keep rows with the expected number of columns
                if len(row) == len(headers):
                    rows.append(row)
            
            # Create DataFrame
            plasmidtype = pd.DataFrame(rows, columns=headers)
        
        # Convert numeric columns to appropriate types
        numeric_cols = ['pident', 'length', 'mismatch', 'gapopen', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore']
        for col in numeric_cols:
            if col in plasmidtype.columns:
                plasmidtype[col] = pd.to_numeric(plasmidtype[col], errors='coerce')
        
        # Print basic info
        print(f"Shape: {plasmidtype.shape}")
        print(f"Columns: {list(plasmidtype.columns)}")
        
        # Convert to CSV format
        sample_name = os.path.splitext(os.path.basename(file_path))[0]
        output_csv = f"{sample_name}_plasmid_results.csv"
        plasmidtype.to_csv(output_csv, index=False)
        
        print(f"Results saved to: {output_csv}")
        if not plasmidtype.empty:
            print(f"First few rows:\n{plasmidtype.head()}")
        else:
            print("Warning: No data found in file")
        print("-" * 80)
        
        return plasmidtype
        
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return None

def main():
    """
    Main function to process all text files in plasmidtyping_out folder
    """
    # Define input directory
    input_dir = "plasmidtyping_out"
    
    # Check if directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Directory '{input_dir}' not found!")
        print("Please make sure the plasmidtyping_out folder exists in the current directory.")
        sys.exit(1)
    
    # Find all text files in the directory
    txt_files = glob.glob(os.path.join(input_dir, "*.txt"))
    
    if not txt_files:
        print(f"No .txt files found in '{input_dir}' directory!")
        sys.exit(1)
    
    print(f"Found {len(txt_files)} text files to process:")
    for file in txt_files:
        print(f"  - {file}")
    print()
    
    # Process each file
    results_summary = []
    
    for txt_file in txt_files:
        result = process_plasmid_file(txt_file)
        if result is not None:
            sample_name = os.path.splitext(os.path.basename(txt_file))[0]
            results_summary.append({
                'sample': sample_name,
                'num_hits': len(result),
                'file_processed': txt_file
            })
    
    # Create summary report
    if results_summary:
        summary_df = pd.DataFrame(results_summary)
        summary_df.to_csv("plasmid_typing_summary.csv", index=False)
        print(f"\nSummary report saved to: plasmid_typing_summary.csv")
        print(f"Total files processed: {len(results_summary)}")
        print("\nSummary:")
        print(summary_df)
    
    print("\nProcessing completed!")

if __name__ == "__main__":
    main()