import pandas as pd

# Input and output file
input_file = "/Merge_MNQ_contracts/merged_files_outputs\\MNQ_merged_spread.csv"
output_file = "MNQ_merged_spread_shifted_back_3_hours.csv"

# Read CSV
print("Reading file:", input_file)
df = pd.read_csv(input_file, sep="\t")

# Combine DATE and TIME into one datetime
print("Combining DATE and TIME into DATETIME")
df["DATETIME"] = pd.to_datetime(df["<DATE>"] + " " + df["<TIME>"], format="%Y.%m.%d %H:%M:%S")

# Shift by -3 hours
print("Shifting DATETIME by +3 hours")
df["DATETIME"] = df["DATETIME"] + pd.Timedelta(hours=3)

# Split back into DATE and TIME
print("Splitting DATETIME back into <DATE> and <TIME>")
df["<DATE>"] = df["DATETIME"].dt.strftime("%Y.%m.%d")
df["<TIME>"] = df["DATETIME"].dt.strftime("%H:%M:%S")

# Drop helper column
print("Dropping helper DATETIME column")
df = df.drop(columns=["DATETIME"])

# Save to new CSV
df.to_csv(output_file, sep="\t", index=False)
print(f"Saved corrected file to {output_file}")
