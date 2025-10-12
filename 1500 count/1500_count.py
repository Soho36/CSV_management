import pandas as pd

# --- Load & clean data ---
df = pd.read_csv("deposit_change_file_from_marketstat.csv", sep="\t")

df['Deposit'] = (
    df['Deposit']
    .astype(str)
    .str.replace(' ', '', regex=False)
    .str.replace(',', '.', regex=False)
    .astype(float)
)

# --- Parameters ---
start_level = 1500
step = 1500
end_level = df['Deposit'].max()

# --- Loop through and calculate ---
rows_per_step = []
current_threshold = start_level
start_index = 0

for i, value in enumerate(df['Deposit']):
    if value >= current_threshold + step:
        rows = i - start_index
        rows_per_step.append((current_threshold, current_threshold + step, rows))
        start_index = i
        current_threshold += step

# --- Output ---
print("Detailed step report:\n")
for start, end, rows in rows_per_step:
    print(f"From {start:,.0f} → {end:,.0f} took {rows} days")

# --- Average ---
if rows_per_step:
    avg_rows = sum(r for _, _, r in rows_per_step) / len(rows_per_step)
    print(f"\nAverage number of rows (days) per +1.5k increase: {avg_rows:.2f}")
else:
    print("No full +1.5k steps found in the data.")
