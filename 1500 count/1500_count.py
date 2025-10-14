import pandas as pd

# --- Load & clean data ---
df = pd.read_csv("../1500 count/csvs/with_pnl.csv", sep="\t")
pd.set_option('display.max_rows', None)

# Clean number formatting
df['P/L (Net)'] = (
    df['P/L (Net)']
    .astype(str)
    .str.replace(' ', '', regex=False)
    .str.replace(',', '.', regex=False)
    .astype(float)
)

# === CONFIG ===
TARGET = 20000       # profit target per run
MAX_DD = 7500       # maximum drawdown allowed before "blowup"
SIZE = 8            # multiplier for each trade's PnL
results = []

# --- Loop through every possible starting date ---
for start_idx in range(len(df)):
    cumulative_pnl = 0
    min_cumulative_pnl = 0
    days = 0
    reached = False
    blown = False

    # Loop forward from this start point
    for i in range(start_idx, len(df)):
        cumulative_pnl += df.loc[i, 'P/L (Net)'] * SIZE
        min_cumulative_pnl = min(min_cumulative_pnl, cumulative_pnl)
        days += 1

        # Check blowup condition first
        if abs(min_cumulative_pnl) >= MAX_DD:
            results.append({
                "Start_Date": df.loc[start_idx, 'Date'],
                "Rows_to_+Target": None,
                "Max_Drawdown": abs(min_cumulative_pnl),
                "End_Date": df.loc[i, 'Date'],
                "Blown": True
            })
            blown = True
            break

        # Check profit target
        if cumulative_pnl >= TARGET:
            results.append({
                "Start_Date": df.loc[start_idx, 'Date'],
                "Rows_to_+Target": days,
                "Max_Drawdown": abs(min_cumulative_pnl),
                "End_Date": df.loc[i, 'Date'],
                "Blown": False
            })
            reached = True
            break

    # If we reach the end without hitting either condition
    if not reached and not blown:
        results.append({
            "Start_Date": df.loc[start_idx, 'Date'],
            "Rows_to_+Target": None,
            "Max_Drawdown": abs(min_cumulative_pnl),
            "End_Date": None,
            "Blown": False
        })

# --- Display results ---
results_df = pd.DataFrame(results)
print(results_df)

# --- Stats ---
valid = results_df.dropna(subset=["Rows_to_+Target"])
if not valid.empty:
    print("\n====== SUMMARY STATS ======")
    print("Target:", TARGET)
    print("Max drawdown allowed:", MAX_DD)
    print("Size multiplier:", SIZE)
    print()
    print("Min days:", valid["Rows_to_+Target"].min())
    print("Max days:", valid["Rows_to_+Target"].max())
    print("Average days:", round(valid["Rows_to_+Target"].mean(), 2))
    print("Median days:", valid["Rows_to_+Target"].median())
    print("Std dev days:", round(valid["Rows_to_+Target"].std(), 2))
    print("Mode days:", valid["Rows_to_+Target"].mode().values)
    print("Count of valid runs:", len(valid))

# --- Probability metrics ---
total_runs = len(results_df)
blowups = len(results_df[results_df["Blown"] == True])
successful = len(valid)

print("\n====== PROBABILITY METRICS ======")
print(f"Total runs: {total_runs}")
print(f"Successful runs: {successful} ({successful / total_runs * 100:.2f}%)")
print(f"Blowups: {blowups} ({blowups / total_runs * 100:.2f}%)")
print(f"Survival probability: {(1 - blowups / total_runs) * 100:.2f}%")

# --- Save results ---
# path_to_save = "pnl_growth_results_target_dd.csv"
# results_df.to_csv(path_to_save, index=False, sep="\t")
# print(f"\nResults saved to {path_to_save}")

# Sheet 2: summary + probability metrics
summary_data = {
    "Metric": [
        "Min days", "Max days", "Average days", "Median days", "Std dev days", "Mode days",
        "Count of valid runs", "Total runs", "Successful runs (%)",
        "Blowups (%)", "Survival probability (%)", "", "Position size multiplier",
        "Target", "Max Drawdown Limit"
    ],
    "Value": [
        valid["Rows_to_+Target"].min() if not valid.empty else None,
        valid["Rows_to_+Target"].max() if not valid.empty else None,
        round(valid["Rows_to_+Target"].mean(), 2) if not valid.empty else None,
        valid["Rows_to_+Target"].median() if not valid.empty else None,
        round(valid["Rows_to_+Target"].std(), 2) if not valid.empty else None,
        valid["Rows_to_+Target"].mode().values[0] if not valid.empty else None,
        len(valid),
        len(results_df),
        f"{len(valid) / len(results_df) * 100:.2f}%" if total_runs > 0 else None,
        f"{blowups / len(results_df) * 100:.2f}%" if total_runs > 0 else None,
        f"{(1 - blowups / len(results_df)) * 100:.2f}%" if total_runs > 0 else None,
        "",
        SIZE,
        TARGET,
        MAX_DD
    ]
}
summary_df = pd.DataFrame(summary_data)

# --- Histogram data ---
if not valid.empty:
    hist_data = (
        valid["Rows_to_+Target"]
        .value_counts()
        .sort_index()
        .reset_index()
        .rename(columns={"index": "Days", "Rows_to_+Target": "Took_days"})
    )
else:
    hist_data = pd.DataFrame(columns=["Days", "Took_days"])

# --- Save all to Excel ---
with pd.ExcelWriter(f"pnl_growth_report_{TARGET}_{MAX_DD}_{SIZE}.xlsx") as writer:
    results_df.to_excel(writer, sheet_name="All Runs", index=False)
    summary_df.to_excel(writer, sheet_name="Summary Stats", index=False)
    hist_data.to_excel(writer, sheet_name="Histogram", index=False)

print("\n✅ Excel report created: pnl_growth_report_with_hist.xlsx")
print("   Sheets: [All Runs, Summary Stats, Histogram]")
