import pandas as pd
import os
# Input and output2 file

input_file = "../TimeShift_TradeHistory/inputs/trade_stats_1_minute.csv"

file_name = os.path.basename(input_file)  # Extract file name from input_file
output_file = f"../TimeShift_TradeHistory/outputs/time_shifted_{file_name}"


# Read Excel
print("Reading file:", input_file)
df = pd.read_csv(input_file, sep="\t", encoding="utf-8")

# Convert 'Time' to datetime
print("Converting 'Entry_time' and 'Exit_time' to datetime")
df["Entry_time"] = pd.to_datetime(df["Entry_time"], format="%Y.%m.%d %H:%M:%S")
df["Exit_time"] = pd.to_datetime(df["Exit_time"], format="%Y.%m.%d %H:%M:%S")

# Shift forward by 3 hours
print("Shifting 'Entry_time' and 'Exit_time' by +3 hours")
df["Entry_time"] = df["Entry_time"] + pd.Timedelta(hours=3)
df["Entry_time"] = df["Entry_time"].dt.strftime("%Y.%m.%d %H:%M:%S")
df["Exit_time"] = df["Exit_time"] + pd.Timedelta(hours=3)
df["Exit_time"] = df["Exit_time"].dt.strftime("%Y.%m.%d %H:%M:%S")

# Save to new Excel
df.to_csv(output_file, index=False, sep="\t", encoding="utf-8")
print(f"Saved corrected file to {output_file}")
