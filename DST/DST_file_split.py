import pandas as pd
from pathlib import Path

# ===============================
# CONFIG
# ===============================
INPUT_CSV = "../DST/MNQ_merged_no_spread.csv"           # your source file
OUTPUT_DIR_SPLITS = "splits"                            # output folder
OUTPUT_DIR_MERGED = "merged"                            # output folder for merged files
MERGE_DST_FILES = True                                  # True = save merged DST / NO_DST, False = skip

# Column names for date and time
date_col = "<DATE>"
time_col = "<TIME>"

# Periods: (start_date, end_date)
periods = [
    ("2019-03-10", "2019-11-03"),
    ("2019-11-03", "2020-03-08"),
    ("2020-03-08", "2020-11-01"),
    ("2020-11-01", "2021-03-14"),
    ("2021-03-14", "2021-11-07"),
    ("2021-11-07", "2022-03-13"),
    ("2022-03-13", "2022-11-06"),
    ("2022-11-06", "2023-03-12"),
    ("2023-03-12", "2023-11-05"),
    ("2023-11-05", "2024-03-10"),
    ("2024-03-10", "2024-11-03"),
    ("2024-11-03", "2025-03-09"),
    ("2025-03-09", "2025-11-02"),
]

# ===============================
# LOAD DATA
# ===============================
print("Reading input CSV...")
try:
    df = pd.read_csv(INPUT_CSV, sep="\t")
except Exception as e:
    print(f"Error reading {INPUT_CSV}: {e}")
    exit(1)

# Combine DATE + TIME → datetime
print("Processing datetime...")
df["datetime"] = pd.to_datetime(
    df[date_col] + " " + df[time_col],
    format="%Y.%m.%d %H:%M:%S"
)

# Sort by datetime
print("Sorting data by datetime...")
df.sort_values("datetime", inplace=True)

# ===============================
# SPLIT & SAVE
# ===============================
Path(OUTPUT_DIR_SPLITS).mkdir(exist_ok=True)

for start, end in periods:
    start_dt = pd.to_datetime(start)
    end_dt = pd.to_datetime(end)

    mask = (df["datetime"] >= start_dt) & (df["datetime"] < end_dt)
    chunk = df.loc[mask].drop(columns=["datetime"])

    # DST vs NO_DST by start month
    prefix = "DST" if start_dt.month == 3 else "NO_DST"

    filename = f"{prefix}_{start}_to_{end}.csv"
    out_path = Path(OUTPUT_DIR_SPLITS) / filename

    try:
        chunk.to_csv(out_path, sep="\t", index=False, encoding="utf-8")
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        continue

    print(f"Saved {filename}: {len(chunk)} rows")

# ===============================
# MERGE LOGIC
# ===============================
if MERGE_DST_FILES:

    print("Merging DST and NO_DST files...")
    dst_frames = []
    no_dst_frames = []

    for file in Path(OUTPUT_DIR_SPLITS).glob("*.csv"):
        if file.name.startswith("DST_"):
            dst_frames.append(pd.read_csv(file, sep="\t"))
        elif file.name.startswith("NO_DST_"):
            no_dst_frames.append(pd.read_csv(file, sep="\t"))

    if dst_frames:
        dst_df = pd.concat(dst_frames, ignore_index=True)
        dst_df["datetime"] = pd.to_datetime(
            dst_df["<DATE>"] + " " + dst_df["<TIME>"],
            format="%Y.%m.%d %H:%M:%S"
        )
        dst_df.sort_values("datetime", inplace=True)
        dst_df.drop(columns="datetime", inplace=True)

        # Ensure the output directory exists
        Path(OUTPUT_DIR_MERGED).mkdir(parents=True, exist_ok=True)
        # Save the file
        dst_df.to_csv(
            Path(OUTPUT_DIR_MERGED) / "DST_ALL.csv",
            sep="\t",
            index=False,
            encoding="utf-8"
        )

        print(f"Saved DST_ALL.csv: {len(dst_df)} rows")

    if no_dst_frames:
        no_dst_df = pd.concat(no_dst_frames, ignore_index=True)
        no_dst_df["datetime"] = pd.to_datetime(
            no_dst_df["<DATE>"] + " " + no_dst_df["<TIME>"],
            format="%Y.%m.%d %H:%M:%S"
        )
        no_dst_df.sort_values("datetime", inplace=True)
        no_dst_df.drop(columns="datetime", inplace=True)

        # Ensure the output directory exists
        Path(OUTPUT_DIR_MERGED).mkdir(parents=True, exist_ok=True)
        no_dst_df.to_csv(
            Path(OUTPUT_DIR_MERGED) / "NO_DST_ALL.csv",
            sep="\t",
            index=False,
            encoding="utf-8"
        )
        print(f"Saved NO_DST_ALL.csv: {len(no_dst_df)} rows")
