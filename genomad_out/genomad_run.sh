#!/bin/bash

# Directory contain input and output
INPUT_DIR="/home/kien1211/Downloads/fasta"
OUTPUT_DIR="/home/kien1211/Downloads/genomad_out"
GENOMAD_DB="/home/kien1211/Downloads/genomad_db"  # Update this path to your actual GeNomad database

# Make output_dir
mkdir -p "$OUTPUT_DIR"

# Check if input directory exists
if [[ ! -d "$INPUT_DIR" ]]; then
    echo "Error: Input directory $INPUT_DIR does not exist"
    exit 1
fi

# Check if GeNomad database exists
if [[ ! -d "$GENOMAD_DB" ]]; then
    echo "Error: GeNomad database not found at $GENOMAD_DB"
    echo "Please download the database with: genomad download-database ."
    exit 1
fi

# Check if any .fasta files exist in input directory
if ! ls "$INPUT_DIR"/*.fasta &>/dev/null; then
    echo "Error: No .fasta files found in $INPUT_DIR"
    exit 1
fi

echo "Starting GeNomad processing..."
echo "Input directory: $INPUT_DIR"
echo "Output directory: $OUTPUT_DIR"
echo "Database: $GENOMAD_DB"

# For loop to run all contigs files
for fasta_file in "$INPUT_DIR"/*.fasta; do
    # Check if files exist
    if [[ -f "$fasta_file" ]]; then
        # Make sample_id from input (remove path and .fasta extension)
        sample_id=$(basename "$fasta_file" .fasta)
        sample_output_dir="$OUTPUT_DIR/${sample_id}"
        
        # Create sample-specific output directory
        mkdir -p "$sample_output_dir"
        
        # Skip if results already exist
        if [[ -f "$sample_output_dir/${sample_id}_summary.tsv" ]]; then
            echo "Skipping $sample_id (results already exist)"
            continue
        fi
        
        echo "Processing: $sample_id"
        
        # Run GeNomad end-to-end
        genomad end-to-end \
            --cleanup \
            --splits 8 \
            --enable-score-calibration \
            "$fasta_file" \
            "$sample_output_dir" \
            "$GENOMAD_DB"
        
        # Check if GeNomad command was successful
        if [[ $? -eq 0 ]]; then
            echo "✅ Output saved: $sample_output_dir"
            
            # List generated files
            echo "Generated files:"
            ls -la "$sample_output_dir"
        else
            echo "❌ Error processing: $sample_id"
        fi
    else
        echo "Skipping: $fasta_file (file not found)"
    fi
done

echo "Finished processing all files"
