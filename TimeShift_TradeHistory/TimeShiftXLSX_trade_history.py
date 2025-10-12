import pandas as pd
import os
# Input and output file

input_file = "../TimeShift_TradeHistory/inputs/1500 start to see number of blowups with 1 contract.xlsx"
file_name = os.path.basename(input_file)  # Extract file name from input_file
output_file = f"../TimeShift_TradeHistory/outputs/time shifted {file_name}"


# Read Excel
print("Reading file:", input_file)
df = pd.read_excel(input_file)

# Convert 'Time' to datetime
print("Converting 'Time' to datetime")
df["Time"] = pd.to_datetime(df["Time"], format="%Y.%m.%d %H:%M:%S")

# Shift forward by 3 hours
print("Shifting 'Time' by +3 hours")
df["Time"] = df["Time"] + pd.Timedelta(hours=3)
df["Time"] = df["Time"].dt.strftime("%Y.%m.%d %H:%M:%S")

# Save to new Excel
df.to_excel(output_file, index=False)
print(f"Saved corrected file to {output_file}")