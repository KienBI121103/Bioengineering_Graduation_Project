#!/bin/bash

# Directory contain input and output
INPUT_DIR="/home/kien1211/Downloads/fasta"
OUTPUT_DIR="/home/kien1211/Downloads/platon_out"


# Make output_dir
mkdir -p "$OUTPUT_DIR"

# For loop to run all contigs files
for fasta_file in "$INPUT_DIR"/*.fasta; do
    # Check if files exist (and handle case where no .fasta files exist)
    if [[ -f "$fasta_file" ]]; then
        # Make sample_id from input (remove path and .fasta extension)
        sample_id=$(basename "$fasta_file" .fasta)
        output_file="$OUTPUT_DIR/${sample_id}"

        # Run Platon
        echo "Processing: $fasta_file"
        platon --db  /home/kien1211/Downloads/db  --output  "$output_file" --verbose  --threads 8 "$fasta_file"

        # Check if PlatonPlaton command was successful
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
