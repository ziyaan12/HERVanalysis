#!/bin/bash

# defijne directories and files
base_dir="/home/zo24/telescope/all"
input_dir="${base_dir}/results"
sorted_dir="${base_dir}/sorted"
telescoperesults_dir="${base_dir}/telescoperesults"
log_dir="${base_dir}/logs"
gtf_file="${base_dir}/HERV_rmsk.hg38.v2.gtf"
process_log="${base_dir}/telescope_process.log"

# create output and log directories
mkdir -p "$sorted_dir" || { echo "Failed to create sorted directory"; exit 1; }
mkdir -p "$telescoperesults_dir" || { echo "Failed to create telescoperesults directory"; exit 1; }
mkdir -p "$log_dir" || { echo "Failed to create log directory"; exit 1; }

# start the process log file
if [ ! -f "$process_log" ]; then
    echo "Process started at $(date)" > "$process_log"
else
    echo "Resuming process at $(date)" >> "$process_log"
fi

# source conda.sh to enable conda commands
echo "Sourcing conda.sh..." >> "$process_log"
source /home/zo24/miniconda3/etc/profile.d/conda.sh || { echo "Failed to source conda.sh" >> "$process_log"; exit 1; }

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

# iterate over Skmel5-10 files
for sam_file in ${input_dir}/Skmel5-10*_R1+2_001.sam; do
  base_name=$(basename "$sam_file" "_R1+2_001.sam")
  sorted_sam_file="${sorted_dir}/sorted_${base_name}_R1+2_001.sam"
  result_subdir="${telescoperesults_dir}/${base_name}"
  log_file="${log_dir}/${base_name}_telescope.log"

  # create result subdirectory
  mkdir -p "$result_subdir" || { echo "Failed to create directory: $result_subdir" >> "$process_log"; exit 1; }

  # check if the telescope output files already exist and skip if they do
  if [ -f "${result_subdir}/telescope-TE_counts.tsv" ] && [ -f "${result_subdir}/telescope-stats_report.tsv" ]; then
    echo "Telescope output files for $base_name already exist, skipping." >> "$process_log"
    continue
  fi

  start_time=$(date)
  echo "Processing file: $base_name" >> "$process_log"
  echo "Start time: $start_time" >> "$process_log"

  # run samtools sort
  samtools_cmd="samtools sort -n -o $sorted_sam_file $sam_file"
  run_command "$samtools_cmd" "$log_file"
  if [ $? -ne 0 ]; then
    echo "Error during samtools sort for $base_name. Check $log_file for details." >> "$process_log"
    continue
  fi

  # activate the telescope_dg environment
  echo "Activating telescope_dg environment..." >> "$process_log"
  conda activate telescope_dg || { echo "Failed to activate telescope_dg environment" >> "$process_log"; exit 1; }

  # run telescope assign
  echo "Running telescope assign for $base_name..." >> "$process_log"
  (cd "$result_subdir" && telescope assign "$sorted_sam_file" "$gtf_file")
  if [ $? -ne 0 ]; then
    echo "Error during telescope assign for $base_name. Check $log_file for details." >> "$process_log"
    conda deactivate
    continue
  fi

  # deactivate the telescope_dg environment
  echo "Deactivating telescope_dg environment..." >> "$process_log"
  conda deactivate || { echo "Failed to deactivate telescope_dg environment" >> "$process_log"; exit 1; }

  end_time=$(date)
  echo "Completed processing for $base_name." >> "$process_log"
  echo "End time: $end_time" >> "$process_log"

  # compress the original SAM file
  gzip "$sam_file" || { echo "Failed to compress $sam_file" >> "$process_log"; exit 1; }
done

echo "Telescope processing complete at $(date). Results are in the $telescoperesults_dir directory." >> "$process_log"
