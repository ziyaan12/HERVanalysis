#!/bin/bash

# define the path to your files
file_path="/home/zo24/telescope/all/igv"
log_file="$file_path/conversion.log"

# create the output directory if it does not exist
mkdir -p "$file_path/bam"

# create the log file
echo "Conversion Log - $(date)" > "$log_file"

# get the list of .sam files sorted alphabetically and numerically
files=$(ls "$file_path"/*.sam | sort -V)

# loop through each SAM file in the specified directory
for file in $files; 
do
    if [ -e "$file" ]; then
        # get the base name of the file
        base_name=$(basename "$file" .sam)
        bam_file="$file_path/bam/${base_name}.sorted.bam"
        bai_file="$bam_file.bai"
        
        if [ -e "$bam_file" ] && [ -e "$bai_file" ]; then
            echo "Skipping $file as BAM and BAI files already exist." | tee -a "$log_file"
            continue
        fi
        
        echo "Processing $file" | tee -a "$log_file"
        
        # convert the SAM file to BAM format
        bam_unsorted="$file_path/bam/${base_name}.bam"
        samtools view -bS "$file" > "$bam_unsorted"
        echo "Converted $base_name to BAM format" | tee -a "$log_file"
        
        # sort the BAM file by coordinate
        samtools sort "$bam_unsorted" -o "$bam_file"
        echo "Sorted BAM file: $bam_file" | tee -a "$log_file"
        
        # index the sorted BAM file
        samtools index "$bam_file"
        echo "Indexed BAM file: $bam_file" | tee -a "$log_file"
        
        # optionally, remove the unsorted BAM file if no longer needed
        rm "$bam_unsorted"
    else
        echo "No .sam files found in $file_path" | tee -a "$log_file"
        exit 1
    fi
done

echo "Processing complete" | tee -a "$log_file"
