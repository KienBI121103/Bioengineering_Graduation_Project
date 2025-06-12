import os
import glob

def wrap_fasta(input_path, output_path, line_length=66):
    """Wrap FASTA sequences to specified line length"""
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if line.startswith(">"):
                outfile.write(line + "\n")
            else:
                for i in range(0, len(line), line_length):
                    outfile.write(line[i:i+line_length] + "\n")

def main():
    input_dir = "/home/kien1211/Downloads/platon_out"
    
    # Find all chromosome FASTA files
    fasta_files = glob.glob(f"{input_dir}/*/*.chromosome.fasta")
    
    print(f"Looking for files in: {input_dir}/*/*.chromosome.fasta")
    print(f"Found {len(fasta_files)} files")
    
    if not fasta_files:
        print("No chromosome FASTA files found!")
        print("Checking directory structure...")
        if os.path.exists(input_dir):
            print(f"Input directory exists: {input_dir}")
            subdirs = [d for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]
            print(f"Subdirectories found: {subdirs}")
            
            # Check contents of subdirectories
            for subdir in subdirs:
                subdir_path = os.path.join(input_dir, subdir)
                if os.path.exists(subdir_path):
                    files = os.listdir(subdir_path)
                    print(f"Files in {subdir}: {files}")
        else:
            print(f"Input directory does not exist: {input_dir}")
        return
    
    for fasta_file in fasta_files:
        print(f"Processing file: {fasta_file}")
        
        # Extract SRR ID from path - Fixed the index
        # Path structure: /home/kien1211/Downloads/platon_out/SRR123/file.chromosome.fasta
        # Split gives: ['', 'home', 'kien1211', 'Downloads', 'platon_out', 'SRR123', 'file.chromosome.fasta']
        # Index -2 gets the SRR directory name
        srr_id = fasta_file.split("/")[-2]
        print(f"Extracted SRR ID: {srr_id}")
        
        # Fixed: Create a logical output path structure
        output_path = os.path.join(input_dir, srr_id, f"{srr_id}_convert_chromosome.fasta")
        
        try:
            # Wrap fasta
            wrap_fasta(fasta_file, output_path)
            print(f"✅ Wrapped: {srr_id} -> {output_path}")
        except FileNotFoundError as e:
            print(f"❌ File not found error for {srr_id}: {e}")
        except PermissionError as e:
            print(f"❌ Permission error for {srr_id}: {e}")
        except Exception as e:
            print(f"❌ Error processing {srr_id}: {e}")

if __name__ == "__main__":
    main()
