import os
import glob

def wrap_fasta(input_path, output_path, line_length=66):
    with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if line.startswith(">"):
                outfile.write(line + "\n")
            else:
                for i in range(0, len(line), line_length):
                    outfile.write(line[i:i+line_length] + "\n")

input_dir = "/home/kien1211/Downloads/platon_out"

# Tìm tất cả các file contigs.chromosome.fasta
fasta_files = glob.glob(f"{input_dir}/*/*.chromosome.fasta")

for fasta_file in fasta_files:
    srr_id = fasta_file.split("/")[-4]
    output_path = os.path.join(input_dir, srr_id, 'Downloads', 'platon_out', f"{srr_id}_convert_chromosome.fasta")
     # Wrap fasta
    wrap_fasta(fasta_file, output_path)
    print(f"✅ Wrapped: {srr_id} -> {output_path}")
    
