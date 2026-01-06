import pandas as pd
import os

# Define the directory containing the files to merge
path_input = "../Merge_MNQ_contracts/files_to_merge_inputs/"

print(f"Combining files: {os.listdir(path_input)}")

# Read and combine all CSVs
dfs = [pd.read_csv(os.path.join(path_input, f), sep='\t') for f in os.listdir(path_input) if f.endswith('.csv')]
df_all = pd.concat(dfs, ignore_index=True)
print(f"Combined DataFrame shape: {df_all.shape}")

# Save final merged file in MT5 format (tab-delimited, same header)
output_path = "../Merge_MNQ_contracts/files_to_merge_outputs/MNQ_merged.csv"
df_all.to_csv(output_path, sep='\t', index=False)

print("Merged file saved as MNQ_merged.csv")
