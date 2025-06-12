#!/bin/bash

# Input_dir and output_dir

INPUT_DIR="/home/kien1211/Downloads/fasta"
REF_GENOME="/home/kien1211/Downloads/Ab_ATCC19606/Ab_ATCC19606.fasta.gz"
REF_GENE="/home/kien1211/Downloads/Ab_ATCC19606/genomic.gff"
OUTPUT_DIR="/home/kien1211/Downloads/quast_out"

# Make output_dir

mkdir -p "$OUTPUT_DIR"

#for loop run all fasta file
for fastafile in "$INPUT_DIR"/*.fasta; do
    #Check if files exist
    if [[ -f "$fastafile" ]]; then
        #Make sample_id from input
        sample_id=$(basename "$fastafile" .fasta)
        output_file="$OUTPUT_DIR/${sample_id}_quast"

       #Run quast
        echo "Processing: $fastafile"
        quast.py -r "$REF_GENOME" -g "$REF_GENE" -o "$output_file"  "$fastafile"
        # Check if QUast  command was successful
        if [[ $? -eq 0 ]]; then
            echo "Output saved: $output_file"
        else
            echo "Error processing: $fasta_file"
        fi
    else
        echo "Skipping: $fasta_file (file not found)"
    fi
done

echo "Finished processing all files"

