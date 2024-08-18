import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_prepare_data(file_path):
    df = pd.read_csv(file_path, sep='\t')
    df.set_index('transcript', inplace=True)
    return df

def create_comparison_visualizations(data, output_base_dir):
    # ensure output directory exists
    comparison_output_dir = os.path.join(output_base_dir, 'comparison')
    if not os.path.exists(comparison_output_dir):
        os.makedirs(comparison_output_dir)

    # calculate the average TPM for the top 25 transcripts
    data['Average_TPM'] = data.mean(axis=1)
    top_25_combined_data = data.nlargest(25, 'Average_TPM').drop(columns=['Average_TPM'])

    # combine the data for seaborn
    top_25_combined_data = top_25_combined_data.reset_index().melt(id_vars=['transcript'], var_name='Group', value_name='TPM')

    # define colors for the groups
    color_palette = {
        'TPM_Skmel5-1-B1R1_S3': 'darkred',
        'TPM_Skmel5-1-B1R2_S2': 'lightcoral',
        'TPM_Skmel5-10-B1R1_S2': 'darkblue',
        'TPM_Skmel5-10-B1R2_S1': 'lightblue'
    }

    plt.figure(figsize=(14, 10))
    sns.barplot(x='TPM', y='transcript', hue='Group', data=top_25_combined_data, dodge=True, palette=color_palette)
    plt.title('Highest Transcripts by Average TPM: Skmel5-1-B1R1_S3, Skmel5-1-B1R2_S2, Skmel5-10-B1R1_S2, Skmel5-10-B1R2_S1')
    plt.xlabel('TPM')
    plt.ylabel('Transcript')
    plt.legend(title='Group')
    plt.tight_layout()
    plt.savefig(os.path.join(comparison_output_dir, 'top_25_transcripts_barplot.png'))
    plt.close()

    # create heatmap of top 50 transcripts by average TPM across groups using seaborn
    top_50_combined_data = data.nlargest(50, 'Average_TPM').drop(columns=['Average_TPM'])
    top_50_combined_data = top_50_combined_data.reset_index().melt(id_vars=['transcript'], var_name='Group', value_name='TPM')
    top_50_combined_data_pivot = top_50_combined_data.pivot(index='transcript', columns='Group', values='TPM')

    plt.figure(figsize=(20, 14))
    sns.heatmap(top_50_combined_data_pivot, annot=True, fmt='.2f', cmap='viridis', annot_kws={"size": 10})
    plt.title('Heatmap of Top 50 Transcripts by Average TPM: Skmel5-1-B1R1_S3, Skmel5-1-B1R2_S2, Skmel5-10-B1R1_S2, Skmel5-10-B1R2_S1')
    plt.xlabel('Group')
    plt.ylabel('Transcript')
    plt.tight_layout()
    plt.savefig(os.path.join(comparison_output_dir, 'top_50_transcripts_heatmap.png'))
    plt.close()

# define base directory containing the common transcripts file
common_file_path = '/home/zo24/telescope/all/averaged_results/top_100_common_transcripts_tpm_counts.tsv'

# define base output directory for the visualizations
output_base_dir = '/home/zo24/telescope/all/averaged_results/visualizations'

# load and prepare the data
data = load_and_prepare_data(common_file_path)

# create the comparison visualizations
create_comparison_visualizations(data, output_base_dir)
