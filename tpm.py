import os
import pandas as pd

#extract the transcript lengths from the gtf reference file
def extract_transcript_lengths(gtf_file):
    transcript_lengths = {}
    with open(gtf_file, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            columns = line.strip().split('\t')
            if columns[2] == 'exon':
                info = columns[8]
                transcript_id = None
                for attribute in info.split(';'):
                    if 'transcript_id' in attribute:
                        transcript_id = attribute.split('"')[1]
                        break
                if transcript_id:
                    exon_length = int(columns[4]) - int(columns[3]) + 1
                    if transcript_id in transcript_lengths:
                        transcript_lengths[transcript_id] += exon_length
                    else:
                        transcript_lengths[transcript_id] = exon_length

#convert the dictinary to a data frame 
    transcript_lengths_df = pd.DataFrame(list(transcript_lengths.items()), columns=['transcript_id', 'length'])
    return transcript_lengths_df

#function to calculate the TPM
def calculate_tpm(counts_file, lengths_df, output_file):
    counts_df = pd.read_csv(counts_file, sep='\t')

    #merge counts and lengths data frames
    merged_df = counts_df.merge(lengths_df, left_on='transcript', right_on='transcript_id')
    #normalise counts by transcript length
    merged_df['norm_counts'] = merged_df['count'] / merged_df['length']
    #calculate the scaling factor for TPM normalisation
    scaling_factor = merged_df['norm_counts'].sum() / 1e6
    #calculate TPM values
    merged_df['TPM'] = merged_df['norm_counts'] / scaling_factor
    #extract transcript ID anf TPM columns then write to an output file
    tpm_df = merged_df[['transcript', 'TPM']]
    tpm_df.to_csv(output_file, sep='\t', index=False)

#create a function to process each subdirectory within the directory
def process_subdirectories(base_dir, gtf_file):
    lengths_df = extract_transcript_lengths(gtf_file)
    
#iterate through each item in the base directory
    for subdir in os.listdir(base_dir):
        subdir_path = os.path.join(base_dir, subdir)
        if os.path.isdir(subdir_path):
            counts_file = os.path.join(subdir_path, 'telescope-TE_counts.tsv')
            if os.path.exists(counts_file):
                output_file = os.path.join(subdir_path, 'telescope_TPM_results.tsv')
                calculate_tpm(counts_file, lengths_df, output_file)
                print(f"Processed {subdir_path}")
            else:
                print(f"Counts file not found in {subdir_path}")

# define base directory and reference file path
base_dir = '/home/zo24/telescope/all/results'
gtf_file = '/home/zo24/telescope/all/HERV_rmsk.hg38.v2.gtf'

# process each one
process_subdirectories(base_dir, gtf_file)
