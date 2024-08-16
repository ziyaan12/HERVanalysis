import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

# load the data
file_path = '/home/zo24/telescope/all/averaged_results/top_100_common_transcripts_tpm_counts.tsv'
df = pd.read_csv(file_path, sep='\t')

# convert the relevant columns to numeric data types, and non-numeric to NaN
df[['TPM_Skmel5-1-B1R1_S3', 'TPM_Skmel5-1-B1R2_S2', 'TPM_Skmel5-10-B1R1_S2', 'TPM_Skmel5-10-B1R2_S1']] = df[['TPM_Skmel5-1-B1R1_S3', 'TPM_Skmel5-1-B1R2_S2', 'TPM_Skmel5-10-B1R1_S2', 'TPM_Skmel5-10-B1R2_S1']].apply(pd.to_numeric, errors='coerce')

# remove any rows with any NaN values
df_clean = df.dropna()

# perform the t-tests for each transcrip
results = []
for index, row in df_clean.iterrows():
    group1 = row[['TPM_Skmel5-1-B1R1_S3', 'TPM_Skmel5-1-B1R2_S2']].to_numpy(dtype=float)
    group2 = row[['TPM_Skmel5-10-B1R1_S2', 'TPM_Skmel5-10-B1R2_S1']].to_numpy(dtype=float)
    t_stat, _ = ttest_ind(group1, group2, equal_var=False)
    log_fold_change = np.log2(np.mean(group1) + 1) - np.log2(np.mean(group2) + 1)
    mean_diff = np.mean(group1) - np.mean(group2)
    if mean_diff > 0:
        significance = 'Higher in 1%'
    else:
        significance = 'Higher in 10%'
    results.append({
        'transcript': row['transcript'],
        't_stat': t_stat,
        'log_fold_change': log_fold_change,
        'significant': significance
    })

# convert the results to DataFrame
results_df = pd.DataFrame(results)

# Benjamini-Hochberg FDR correction based on t-test
results_df = results_df.sort_values('t_stat', ascending=False)
n = len(results_df['t_stat'])
results_df['rank'] = np.arange(1, n+1)
results_df['BH_FDR'] = results_df['rank'] / n * 0.05
results_df['significant'] = results_df.apply(lambda x: f"{x['significant']} (Significant)" if x['rank'] <= n * 0.05 else f"{x['significant']} (Not Significant)", axis=1)

# save the results
output_path = '/home/zo24/telescope/all/averaged_results/comparison/t_test_results_with_5_percent_FDR.tsv'
results_df_final = results_df[['transcript', 't_stat', 'log_fold_change', 'significant']]
results_df_final.to_csv(output_path, sep='\t', index=False)

print(f"Results have been saved to '{output_path}'")
