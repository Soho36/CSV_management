import pandas as pd

# Input and output2 file
input_file = "../TimeShift_OHLC/input/NO_DST_ALL.csv"
output_file = "../TimeShift_OHLC/output/NO_DST_ALL_shifted.csv"
shift_hours = 2     # Shift by +3 hours for DST and +2 hours for No_DST

# Read CSV
print("Reading file:", input_file)
try:
    df = pd.read_csv(input_file, sep="\t")
except Exception as e:
    print(f"Error reading {input_file}: {e}")
    exit(1)

# Combine DATE and TIME into one datetime
print("Combining DATE and TIME into DATETIME")
df["DATETIME"] = pd.to_datetime(df["<DATE>"] + " " + df["<TIME>"], format="%Y.%m.%d %H:%M:%S")

# Shift by -3 hours
print("Shifting DATETIME by +3 hours")
df["DATETIME"] = df["DATETIME"] + pd.Timedelta(shift_hours, unit="hours")

# Split back into DATE and TIME
print("Splitting DATETIME back into <DATE> and <TIME>")
df["<DATE>"] = df["DATETIME"].dt.strftime("%Y.%m.%d")
df["<TIME>"] = df["DATETIME"].dt.strftime("%H:%M:%S")

# Drop helper column
print("Dropping helper DATETIME column")
df = df.drop(columns=["DATETIME"])

# Save to new CSV
try:
    df.to_csv(output_file, sep="\t", index=False)
    print(f"Saved file to {output_file}")
except Exception as e:
    print(f"Error saving {output_file}: {e}")
    exit(1)
