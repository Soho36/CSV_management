import pandas as pd

# --- Load & clean data ---
df = pd.read_csv("csvs/with_pnl.csv", sep="\t")
pd.set_option('display.max_rows', None)

# Clean number formatting
df['P/L (Net)'] = (
    df['P/L (Net)']
    .astype(str)
    .str.replace(' ', '', regex=False)
    .str.replace(',', '.', regex=False)
    .astype(float)
)

step = 1500  # profit target per run
results = []

# --- Loop through every possible starting date ---
for start_idx in range(len(df)):
    cumulative_pnl = 0
    min_cumulative_pnl = 0  # track the lowest cumulative value (drawdown)
    days = 0
    reached = False

    # Loop forward from this start point
    for i in range(start_idx, len(df)):
        cumulative_pnl += df.loc[i, 'P/L (Net)']
        min_cumulative_pnl = min(min_cumulative_pnl, cumulative_pnl)  # update drawdown
        days += 1

        # Check if profit target is hit
        if cumulative_pnl >= step:
            results.append({
                "Start_Date": df.loc[start_idx, 'Date'],
                "Rows_to_+1.5k": days,
                "Max_Drawdown": abs(min_cumulative_pnl),
                "End_Date": df.loc[i, 'Date']
            })
            reached = True
            break

    # If we reach the end without hitting +1.5k
    if not reached:
        results.append({
            "Start_Date": df.loc[start_idx, 'Date'],
            "Rows_to_+1.5k": None,
            "Max_Drawdown": abs(min_cumulative_pnl),
            "End_Date": None
        })

# --- Display results ---
results_df = pd.DataFrame(results)
print(results_df)

# Optional: Save to file
results_df.to_csv("pnl_growth_results_with_dd.csv", index=False, sep="\t")

# --- Stats on valid runs ---
valid = results_df.dropna(subset=["Rows_to_+1.5k"])
if not valid.empty:
    print("\n====== SUMMARY STATS ======")
    print("Min days:", valid["Rows_to_+1.5k"].min())
    print("Max days:", valid["Rows_to_+1.5k"].max())
    print("Average days:", round(valid["Rows_to_+1.5k"].mean(), 2))
    print("Median days:", valid["Rows_to_+1.5k"].median())
    print("Std dev days:", round(valid["Rows_to_+1.5k"].std(), 2))
    print("Mode days:", valid["Rows_to_+1.5k"].mode().values)
    print("Count of valid runs:", len(valid))
    print("Percentage of runs with drawdown >=1500:",
          round(len(valid[valid["Max_Drawdown"] >= 1500]) / len(valid) * 100, 2), "%")

    print("\n--- DRAWDOWN STATS ---")
    print("Min drawdown:", valid["Max_Drawdown"].min())
    print("Max drawdown:", valid["Max_Drawdown"].max())
    print("Average drawdown:", round(valid["Max_Drawdown"].mean(), 2))
    print("Count of valid runs:", len(valid))
    print("Count of runs with drawdown >=1500:", len(valid[valid["Max_Drawdown"] >= 1500]))
else:
    print("\nNo cases reached +1.5k PnL.")

total_runs = len(results_df)
valid_runs = len(valid)
blowups = len(valid[valid["Max_Drawdown"] >= 1500])
safe_runs = len(valid[valid["Max_Drawdown"] < 1500])

print("\n====== PROBABILITY METRICS ======")
print(f"Total runs: {total_runs}")
print(f"Valid runs (hit +1.5k): {valid_runs}")
print(f"Safe runs (no blowup before +1.5k): {safe_runs}")
print(f"Blowup runs (DD ≥ 1500): {blowups}")

# Probability metrics
print(f"\nSuccess probability (reach +1.5k without blowing up): "
      f"{round(safe_runs / total_runs * 100, 2)}%")

print(f"Blowup probability (DD ≥ 1500 before +1.5k): "
      f"{round(blowups / total_runs * 100, 2)}%")

print(f"Conditional success probability (given you reached +1.5k): "
      f"{round(safe_runs / valid_runs * 100, 2)}%")

