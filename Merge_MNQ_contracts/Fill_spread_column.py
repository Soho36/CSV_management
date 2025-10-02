import pandas as pd

# Input and output file paths
input_file = "merged_files/MNQ_merged.csv"
output_file = "merged_files/MNQ_merged_spread.csv"

# Read CSV (tab-delimited)
print("Reading file:", input_file)
df = pd.read_csv(input_file, sep='\t')

# Fill <SPREAD> column with 1
print("Filling <SPREAD> column with 1")
df['<SPREAD>'] = 1

# Save back to CSV with same delimiter and header
print("Saving updated file to:", output_file)
df.to_csv(output_file, sep='\t', index=False)
