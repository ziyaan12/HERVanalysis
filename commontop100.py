import os
import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path, sep='\t')

def filter_transcripts(df, transcripts):
    return df[df['transcript'].isin(transcripts)]

def save_filtered_data(df, output_path):
    df.to_csv(output_path, sep='\t', index=False)

# define the file paths
base_dir = "/home/zo24/telescope/all/averaged_results"
primary_group_file = os.path.join(base_dir, "Skmel5-1-B1R1_S3_top_100_tpm.tsv")
other_group_files = [
    os.path.join(base_dir, "Skmel5-1-B1R2_S2_filtered_avg_tpm.tsv"),
    os.path.join(base_dir, "Skmel5-10-B1R1_S2_filtered_avg_tpm.tsv"),
    os.path.join(base_dir, "Skmel5-10-B1R2_S1_filtered_avg_tpm.tsv")
]

# load the group data
primary_df = load_data(primary_group_file)
top_100_transcripts = primary_df['transcript'].tolist()

# filter other groups based on top 100 transcripts from primary group
for file_path, label in zip(other_group_files, ["Skmel5-1-B1R2_S2", "Skmel5-10-B1R1_S2", "Skmel5-10-B1R2_S1"]):
    group_df = load_data(file_path)
    filtered_df = filter_transcripts(group_df, top_100_transcripts)
    output_path = os.path.join(base_dir, f"{label}_top_100_tpm.tsv")
    save_filtered_data(filtered_df, output_path)

# create a combined file with all groups
combined_df = primary_df[['transcript', 'TPM']].rename(columns={"TPM": "TPM_Skmel5-1-B1R1_S3"})
for file_path, label in zip(other_group_files, ["Skmel5-1-B1R2_S2", "Skmel5-10-B1R1_S2", "Skmel5-10-B1R2_S1"]):
    group_df = load_data(file_path)
    group_df = filter_transcripts(group_df, top_100_transcripts)
    group_df = group_df.rename(columns={"TPM": f"TPM_{label}"})
    combined_df = pd.merge(combined_df, group_df[['transcript', f"TPM_{label}"]], on="transcript")

output_path = os.path.join(base_dir, "top_100_common_transcripts_tpm_counts.tsv")
combined_df.to_csv(output_path, sep='\t', index=False)
