import pandas as pd
import os
import glob

def process_plasmid_files(input_folder='plasmidtyping_out', output_folder='processed_results'):
    """
    Process all .txt files in the input folder and add headers
    
    Args:
        input_folder (str): Path to folder containing .txt files
        output_folder (str): Path to folder where processed CSV files will be saved
    """
    
    # Define headers for the plasmid typing results
    headers = ['qseqid', 'sseqid', 'pident', 'length', 'mismatch', 
               'gapopen', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore']
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Get all .txt files in the input folder
    txt_files = glob.glob(os.path.join(input_folder, '*.txt'))
    
    if not txt_files:
        print(f"No .txt files found in {input_folder}")
        return
    
    print(f"Found {len(txt_files)} .txt files to process")
    
    processed_files = []
    
    for file_path in txt_files:
        try:
            # Get filename without extension for output naming
            filename = os.path.basename(file_path)
            base_name = os.path.splitext(filename)[0]
            
            print(f"Processing: {filename}")
            
            # Read the file
            with open(file_path, 'r') as f:
                rows = [line.strip().split() for line in f if line.strip()]
            
            # Skip empty files
            if not rows:
                print(f"  Warning: {filename} is empty, skipping...")
                continue
            
            # Create DataFrame with headers
            df = pd.DataFrame(rows, columns=headers)
            
            # Display basic info about the file
            print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")
            
            # Save as CSV
            output_path = os.path.join(output_folder, f"{base_name}.csv")
            df.to_csv(output_path, index=False)
            
            processed_files.append(output_path)
            print(f"  Saved: {output_path}")
            
        except Exception as e:
            print(f"  Error processing {filename}: {str(e)}")
    
    print(f"\nProcessing complete! {len(processed_files)} files processed successfully.")
    return processed_files
# Main execution
if __name__ == "__main__":
    # Option 1: Process all files in a folder
    print("=== Processing all files in plasmidtyping_out folder ===")
    processed_files = process_plasmid_files('plasmidtyping_out', 'processed_results')
    