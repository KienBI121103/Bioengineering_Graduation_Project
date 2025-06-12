#!/bin/bash

# Directory contain input and output
INPUT_DIR="/home/kien1211/Downloads/fasta"
OUTPUT_DIR="/home/kien1211/Downloads/plasmidtyping_out"
# Plasmid_type database
QUERY_FILE="/home/kien1211/Downloads/acinetobacterplasmidtype_feb2025.fasta"

# Make output_dir
mkdir -p "$OUTPUT_DIR"

# Check if query file exists
if [[ ! -f "$QUERY_FILE" ]]; then
    echo "Error: Query file $QUERY_FILE not found!"
    exit 1
fi

# Check if input directory exists
if [[ ! -d "$INPUT_DIR" ]]; then
    echo "Error: Input directory $INPUT_DIR does not exist"
    exit 1
fi

# Check if any .fasta files exist in input directory
if ! ls "$INPUT_DIR"/*.fasta &>/dev/null; then
    echo "Error: No .fasta files found in $INPUT_DIR"
    exit 1
fi

echo "Starting plasmid typing with BLAST..."
echo "Query file: $QUERY_FILE"
echo "Input directory: $INPUT_DIR"
echo "Output directory: $OUTPUT_DIR"

# For loop to run all contigs files
for fasta_file in "$INPUT_DIR"/*.fasta; do
    # Check if files exist (and handle case where no .fasta files exist)
    if [[ -f "$fasta_file" ]]; then
        # Make sample_id from input (remove path and .fasta extension)
        sample_id=$(basename "$fasta_file" .fasta)
        output_file="$OUTPUT_DIR/${sample_id}_plasmidtyping.txt"
        
        # Run Blastn
        echo "Processing: $fasta_file"
        blastn -query "$QUERY_FILE" -subject "$fasta_file" -outfmt 6 -out "$output_file" -perc_identity 95 -num_threads 8
        
        # Check if BLAST command was successful
        if [[ $? -eq 0 ]]; then
            echo "Output saved: $output_file"
            # Check if any results were found
            if [[ -s "$output_file" ]]; then
                result_count=$(wc -l < "$output_file")
                echo "  Found $result_count BLAST hits"
            else
                echo "  No significant hits found"
            fi
        else
            echo "Error processing: $fasta_file"
        fi
    else
        echo "Skipping: $fasta_file (file not found)"
    fi
done

echo "Finished processing all files"
