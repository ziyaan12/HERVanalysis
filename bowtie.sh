#!/bin/bash

# define the directories and files
base_dir="/home/zo24/telescope/all"
input_dir="${base_dir}/input"
output_dir="${base_dir}/results"
log_dir="${base_dir}/logs"
reference="${base_dir}/refs/hg38"
process_log="${base_dir}/process.log"

# create the output and log directories
mkdir -p "$output_dir" || { echo "Failed to create output directory"; exit 1; }
mkdir -p "$log_dir" || { echo "Failed to create log directory"; exit 1; }

# start the the process log file
if [ ! -f "$process_log" ]; then
    echo "Process started at $(date)" > "$process_log"
else
    echo "Resuming process at $(date)" >> "$process_log"
fi

# source conda.sh to enable conda commands
echo "Sourcing conda.sh..." >> "$process_log"
source /home/zo24/miniconda3/etc/profile.d/conda.sh || { echo "Failed to source conda.sh"; exit 1; }

# activate the singleloc_align environment
echo "Activating singleloc_align environment..." >> "$process_log"
conda activate singleloc_align || { echo "Failed to activate singleloc_align environment"; exit 1; }

# define the base names for the file pairs
base_names=(
  "Skmel5-10-B1R1_S2_L001"
)

# create function to run commands and log output
run_command() {
  local cmd="$1"
  local log_file="$2"
  echo "Running: $cmd" >> "$process_log"
  eval "$cmd" >> "$log_file" 2>&1
  local status=$?
  if [ $status -ne 0 ]; then
    echo "Error: Command failed - $cmd" >> "$process_log"
    return 1
  fi
  return 0
}

# total number of files to process
total_files=${#base_names[@]}
current_file=0

# loop through each base name and run Bowtie2 alignment
for base_name in "${base_names[@]}"; do
  current_file=$((current_file + 1))
  r1_file="${input_dir}/${base_name}_R1_001.fastq.gz"
  r2_file="${input_dir}/${base_name}_R2_001.fastq.gz"
  sam_file="${output_dir}/${base_name}_R1+2_001.sam"
  log_file="${log_dir}/${base_name}.log"

  # check if the SAM file already exists and skip if it does
  if [ -f "$sam_file" ]; then
    echo "SAM file for $base_name already exists, skipping." >> "$process_log"
    continue
  fi

  start_time=$(date)
  echo "Processing file $current_file of $total_files: $base_name" >> "$process_log"
  echo "Start time: $start_time" >> "$process_log"

  # run Bowtie2 alignment
  bowtie2_cmd="bowtie2 -k 100 --very-sensitive-local --score-min 'L,0,1.6' --rg-id $base_name -x $reference -1 $r1_file -2 $r2_file -S $sam_file"
  run_command "$bowtie2_cmd" "$log_file"
  if [ $? -ne 0 ]; then
    echo "Error during Bowtie2 alignment for $base_name. Check $log_file for details." >> "$process_log"
    continue
  fi

  end_time=$(date)
  echo "Completed processing for $base_name." >> "$process_log"
  echo "End time: $end_time" >> "$process_log"
done

echo "Bowtie2 processing complete at $(date). Processed $total_files files. Results are in the $output_dir directory." >> "$process_log"
