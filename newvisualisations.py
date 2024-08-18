import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def create_visualizations(file_path, output_base_dir):
    df = pd.read_csv(file_path, sep='\t')

    group_names = df.columns[1:]
    for group_name in group_names:
        group_output_dir = os.path.join(output_base_dir, group_name)
        
        if not os.path.exists(group_output_dir):
            os.makedirs(group_output_dir)

        # extract the TPM values for the current group
        tpm_values = df[group_name].to_numpy()
        print(f"Processing {group_name} - TPM values: {tpm_values[:5]}...")
        print(f"TPM values type: {type(tpm_values)}, shape: {tpm_values.shape}")

        # histogram of TPM values using matplotlib
        plt.figure(figsize=(10, 6))
        plt.hist(tpm_values, bins=20, edgecolor='k', alpha=0.7)
        plt.title(f'TPM Distribution for {group_name}')
        plt.xlabel('TPM')
        plt.ylabel('Frequency')
        plt.savefig(os.path.join(group_output_dir, f'{group_name}_tpm_distribution.png'))
        plt.close()

        # boxplot of TPM values using matplotlib
        plt.figure(figsize=(10, 6))
        plt.boxplot(tpm_values, vert=False)
        plt.title(f'TPM Boxplot for {group_name}')
        plt.xlabel('TPM')
        plt.savefig(os.path.join(group_output_dir, f'{group_name}_tpm_boxplot.png'))
        plt.close()

        # bar plot of top 30 transcripts by TPM using seaborn and matplotlib
        top_50_df = df.nlargest(30, group_name)
        plt.figure(figsize=(18, 10))
        sns.barplot(x=group_name, y='transcript', data=top_50_df)
        plt.title(f'Top 30 Transcripts by TPM for {group_name}')
        plt.xlabel('TPM')
        plt.ylabel('Transcript')
        plt.savefig(os.path.join(group_output_dir, f'{group_name}_top_30_transcripts.png'))
        plt.close()

        # pie chart of top 10 transcripts by TPM using matplotlib
        plt.figure(figsize=(16, 12))
        def make_autopct(values):
            def my_autopct(pct):
                total = sum(values)
                val = pct * total / 100.0
                return '{p:.1f}%\n({v:.2f})'.format(p=pct, v=val)
            return my_autopct
        
        top_10_df = df.nlargest(10, group_name)
        wedges, texts, autotexts = plt.pie(top_10_df[group_name], labels=None, autopct=make_autopct(top_10_df[group_name]), startangle=140, textprops=dict(color="black"))

        plt.setp(autotexts, size=10, weight="bold")
        
        # add labels to piechart
        bbox_props = dict(boxstyle="square,pad=0.3", fc="white", ec="k", lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle="-"),
                  bbox=bbox_props, zorder=0, va="center")

        for i, (p, transcript) in enumerate(zip(wedges, top_10_df['transcript'])):
            ang = (p.theta2 - p.theta1)/2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ang)
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            plt.annotate(transcript, xy=(x, y), xytext=(1.1*np.sign(x), 1.1*y),
                         horizontalalignment=horizontalalignment, **kw)

        plt.title(f'Top 10 Transcripts by TPM for {group_name}', size=16, weight="bold")
        plt.savefig(os.path.join(group_output_dir, f'{group_name}_top_10_transcripts_pie.png'))
        plt.close()

# define the path to the common top 100 transcripts file
file_path = '/home/zo24/telescope/all/averaged_results/top_100_common_transcripts_tpm_counts.tsv'

# define base output directory for the visualizations
output_base_dir = os.path.join(os.path.dirname(file_path), 'finalvisualisations')

# create visualizations
create_visualizations(file_path, output_base_dir)
