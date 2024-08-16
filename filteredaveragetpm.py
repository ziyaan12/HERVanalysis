import os
import pandas as pd

#function to read the TPM files
def read_tpm_files(file_paths):
    dataframes = []
    for file_path in file_paths:
        df = pd.read_csv(file_path, sep='\t')
        dataframes.append(df)
    return dataframes

#function to average the TPM values across multiple data frames
def average_tpm(dataframes):
    combined_df = pd.concat(dataframes)
    avg_tpm_df = combined_df.groupby('transcript', as_index=False).mean()
    return avg_tpm_df

# Filter out transcripts with zero TPM
def filter_zero_tpm(avg_tpm_df):
    filtered_df = avg_tpm_df[avg_tpm_df['TPM'] > 0]
    return filtered_df

#function to process the files, average TPM values and save to an output
def process_groups(base_dir, groups, output_dir):
    for group_name, file_names in groups.items():
        file_paths = [os.path.join(base_dir, file_name, 'telescope_TPM_results.tsv') for file_name in file_names]
        dataframes = read_tpm_files(file_paths)
        avg_tpm_df = average_tpm(dataframes)
        filtered_tpm_df = filter_zero_tpm(avg_tpm_df)
        group_file_name = "_".join(file_names[0].split('_')[:-1])
        output_file = os.path.join(output_dir, f'{group_file_name}_filtered_avg_tpm.tsv')
        filtered_tpm_df.to_csv(output_file, sep='\t', index=False)
        print(f"Processed {group_name}, results saved to {output_file}")

# define the base directory
base_dir = '/home/zo24/telescope/all/results'

# define output directory for the averaged TPM files
output_dir = '/home/zo24/telescope/all/averaged_results'
os.makedirs(output_dir, exist_ok=True)

# define the groups with corresponding subdirectory names
groups = {
    'group1': [
        'Skmel5-1-B1R1_S3_L001',
        'Skmel5-1-B1R1_S3_L002',
        'Skmel5-1-B1R1_S3_L003',
        'Skmel5-1-B1R1_S3_L004'
    ],
    'group2': [
        'Skmel5-1-B1R2_S2_L001',
        'Skmel5-1-B1R2_S2_L002',
        'Skmel5-1-B1R2_S2_L003',
        'Skmel5-1-B1R2_S2_L004'
    ],
    'group3': [
        'Skmel5-10-B1R1_S2_L001',
        'Skmel5-10-B1R1_S2_L002',
        'Skmel5-10-B1R1_S2_L003',
        'Skmel5-10-B1R1_S2_L004'
    ],
    'group4': [
        'Skmel5-10-B1R2_S1_L001',
        'Skmel5-10-B1R2_S1_L002',
        'Skmel5-10-B1R2_S1_L003',
        'Skmel5-10-B1R2_S1_L004'
    ]
}

# process each group and calculate their average TPM values
process_groups(base_dir, groups, output_dir)
