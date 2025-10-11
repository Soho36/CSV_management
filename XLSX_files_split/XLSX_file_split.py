import pandas as pd
import math

# Input file
input_file = "output/output_flatten at 14 and window shifted to local.xlsx"

# Output base name
output_base = "trades_part"

# How many rows per split
rows_per_file = 4001    # Adjusted to 4001 to ensure the last order is "OUT"

# Read the Excel file
df = pd.read_excel(input_file)
print("Reading file:", input_file)

# Calculate how many parts we need
num_parts = math.ceil(len(df) / rows_per_file)
print("Calculating number of parts:", num_parts)

# Split into chunks and save
for i in range(num_parts):
    start = i * rows_per_file
    end = start + rows_per_file
    chunk = df.iloc[start:end]

    output_file = f"{output_base}_{i + 1}.xlsx"
    chunk.to_excel(output_file, index=False)
    print(f"Saved {output_file} with {len(chunk)} rows")
