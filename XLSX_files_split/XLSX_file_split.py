import pandas as pd
import math
import os

# Input file
input_file = "../XLSX_files_split/inputs/time_shifted_100.xlsx"
file_name = os.path.basename(input_file)  # Extract file name from input_file
# Output base name
output_base = f"trades_part_{file_name}"

# How many rows per split
rows_per_file = 4001    # Adjusted to 4001 to ensure the last order is "OUT"

# Read the Excel file
df = pd.read_excel(input_file)
print("Reading file:", input_file)

# Calculate how many parts we need
num_parts = math.ceil(len(df) / rows_per_file)
print("Calculating number of parts:", num_parts)
folder_name = "output99"

os.makedirs(folder_name, exist_ok=True)
# Split into chunks and save
for i in range(num_parts):
    start = i * rows_per_file
    end = start + rows_per_file
    chunk = df.iloc[start:end]

    output_file = f"{folder_name}/{i + 1}_{output_base}"
    chunk.to_excel(output_file, index=False)
    print(f"Saved {output_file} with {len(chunk)} rows")
