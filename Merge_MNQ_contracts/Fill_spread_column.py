import pandas as pd

# Input and output2 file paths
input_file = "../Merge_MN_contracts/merged_files_outputs/MNQ_merged.csv"
output_file = "../Merge_MN_contracts/merged_files_outputs/MNQ_merged_no_spread.csv"

# Read CSV (tab-delimited)
print("Reading file:", input_file)
try:
    df = pd.read_csv(input_file, sep='\t')
except Exception as e:
    print("Error reading the file:", e)
    exit(1)

# Fill <SPREAD> column with 1
print("Filling <SPREAD> column with 1")
df['<SPREAD>'] = 1

# Save back to CSV with same delimiter and header
print("Saving updated file to:", output_file)
try:
    df.to_csv(output_file, sep='\t', index=False)
    print("File saved successfully!")
except Exception as e:
    print("Error saving the file:", e)
    exit(1)

