import pandas as pd

# List your contract CSV files here
files = [
    "cont1.csv",
    "cont2.csv",
    "cont3.csv",
    "cont4.csv",
    "cont5.csv",
    "cont6.csv",
    "cont7.csv",
    "cont8.csv",
]

print(f"Combining files: {files}")

# Read and combine all CSVs
dfs = [pd.read_csv(f, sep='\t') for f in files]
df_all = pd.concat(dfs, ignore_index=True)

print(f"Combined DataFrame shape: {df_all.shape}")

# Save final merged file in MT5 format (tab-delimited, same header)
df_all.to_csv("MNQ_merged.csv", sep='\t', index=False)

print("Merged file saved as MNQ_merged.csv")
