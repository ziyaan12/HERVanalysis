### HERVanalysis

## Coding scripts and other supplementary material used the study of 'Characterising the ERV retro-transcriptome' in stressed cells. Each file/script is listed in chronological order.

HERV_rmsk.hg38..v2.gtf is the gtf file used as a reference for the mapping.

telescope_dg.yml is a script containing the information needed for the creation of the Telescope Conda environment

bowtie.sh is the shell script designed to iterate through the input files, with the sensitive local alignment parameters (requires the creation of a bowtie2 conda environment, details for the environment on https://github.com/mlbendall/telescope_demo) creating the output SAM files needed for Telescope

1telescope.sh and 10telescope.sh iterate through the 1% and 10% Skmel5 SAM files repsectively, name sorting them using samtools before aligning the reads to the gtf reference file mentioned before. The telescope conda environment is activated and the 'Telescope assign' command is run, outputting the results to their own directories and deactivating the conda environment once the process is complete.

tpm.py reads all the telescope output files and calculates the Transcript per Million metric to account for the difference in sequencing depth along the input files.

averagetpm.py categorises the input data, creating average TPM scores for each group (B1R1 and B1R2 from the 1% group, B1R1 and B1R2 from the 10% group) and then removing any null counts

commontop100.py takes the top 100 transcripts (by TPM count) from the Skmel 1% B1R1 group (using this group as a reference) and writes their TPM counts from the other 3 groups, creating a singe file (called top_common_transcripts_tpm_counts.tsv) containing the top 100 TPM results across all 4 groups

newvisualisations.py is the script that creates the visualisations for the individual groups. its reads the data from top_common_transcripts_tpm_counts.tsv and creates pie charts, bar charts, box plots and TPM distribution plots, however only the pie charts and bar charts were used in this study

newcomparisons.py is the script that creates the comparison visualisations. It creates a bar plot and heatmap that present all 4 data groups on the same plot

fdr.py carries out t-test and log fold change calculations for all the 100 transcripts and categorises each transcript based on its result ‘Higher in the 1% group (significantly)’, ‘Higher in the 10% group (significantly)’ or ‘Higher in the 1% group (not significantly)’ or ‘Higher in the 10% group (not significantly)’, creating the file t_test_results_with_5_percent_FDR.tsv

the 5 transcripts that were labelled 'Higher in the 1% group (Significantly) were searched on BioMart, as well as 1 transcript categorised as 'Higher in the 10% group (not Significantly)' included for its exceptionally low t-test and log fold change results

allgenes.txt is the list of genes obtained from the BioMart search of these transcript locations

igv.sh is the shell script designed to iterate through the SAM files from the bowtie2 script earlier and sort them by coordinates, before converting them to BAM format with thier respective input files so that they can be used for visualisation on Integrative Genomics Viewer (IGV)

## note: if attempting this study using the original 32 Skmel5 files (16 1% and 16 10% files, a minimum storage of approximately 1tb is recommended

