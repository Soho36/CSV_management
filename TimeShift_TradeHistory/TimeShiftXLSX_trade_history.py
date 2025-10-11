import pandas as pd

# Input and output file
input_file = "/TimeShift_TradeHistory/output_flatten at 14 and window.xlsx"
output_file = "../XLSX_files_split/output/output_flatten at 14 and window shifted to local.xlsx"

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