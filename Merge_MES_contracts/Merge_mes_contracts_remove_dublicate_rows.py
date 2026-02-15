import pandas as pd
import glob
import os


def merge_futures_csv_files(input_folder=".", output_file="MES_merged_futures.csv"):
    """
    Merge multiple futures CSV files into one, removing overlapping rows.

    Parameters:
    input_folder: folder containing the CSV files (default: current directory)
    output_file: name of the output merged file
    """

    # Get all CSV files in the input folder
    csv_files = glob.glob(os.path.join(input_folder, "*.csv"))

    if not csv_files:
        print(f"No CSV files found in {input_folder}")
        return

    print(f"Found {len(csv_files)} CSV files")

    # List to store all dataframes
    dfs = []

    # Read each CSV file
    for i, file in enumerate(csv_files):
        try:
            # Read the CSV file
            df = pd.read_csv(file, encoding="utf-8", sep='\t')  # Assuming tab-separated values

            # Create a datetime column for easier sorting
            df['DATETIME'] = pd.to_datetime(df['<DATE>'] + ' ' + df['<TIME>'])

            # Store the filename for reference (optional)
            df['SOURCE_FILE'] = os.path.basename(file)

            dfs.append(df)
            print(f"Read {os.path.basename(file)}: {len(df)} rows")

        except Exception as e:
            print(f"Error reading {file}: {e}")

    if not dfs:
        print("No dataframes were created")
        return

    # Combine all dataframes
    combined_df = pd.concat(dfs, ignore_index=True)
    print(f"\nCombined dataframe: {len(combined_df)} rows")

    # Sort by datetime
    combined_df = combined_df.sort_values('DATETIME')

    # Remove duplicates based on datetime (keep first occurrence)
    # This handles the overlapping periods
    combined_df = combined_df.drop_duplicates(subset=['DATETIME'], keep='first')

    print(f"After removing duplicates: {len(combined_df)} rows")

    # Sort again to ensure proper order
    combined_df = combined_df.sort_values('DATETIME')

    # Reset index
    combined_df = combined_df.reset_index(drop=True)

    # Remove the temporary datetime column if you don't want it in output
    # combined_df = combined_df.drop('DATETIME', axis=1)

    # Reorder columns to match original structure
    original_columns = ['<DATE>', '<TIME>', '<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>',
                        '<TICKVOL>', '<VOL>', '<SPREAD>']

    # Add back the datetime column if you want to keep it
    final_columns = original_columns + ['DATETIME', 'SOURCE_FILE']

    # Save to CSV
    combined_df.to_csv(output_file, sep='\t', index=False)
    print(f"\nMerged file saved as: {output_file}")

    # Display some statistics
    print(f"\nDate range: {combined_df['<DATE>'].min()} to {combined_df['<DATE>'].max()}")
    print(f"Total rows: {len(combined_df)}")

    return combined_df


# Alternative approach: More control over which rows to keep
def merge_futures_with_preference(input_folder=".", output_file="MES_merged_futures.csv",
                                  prefer_later_contract=True):
    """
    Merge futures files with option to prefer data from later or earlier contracts
    when overlaps occur.

    Parameters:
    prefer_later_contract: if True, keep data from later contracts when overlapping
                          if False, keep data from earlier contracts
    """

    csv_files = sorted(glob.glob(os.path.join(input_folder, "*.csv")))

    if not csv_files:
        print(f"No CSV files found in {input_folder}")
        return

    # Read all files and add contract order information
    dfs = []
    for i, file in enumerate(csv_files):
        df = pd.read_csv(file, sep='\t')
        df['DATETIME'] = pd.to_datetime(df['DATE'] + ' ' + df['TIME'])
        df['CONTRACT_ORDER'] = i  # Lower number = earlier contract
        df['SOURCE_FILE'] = os.path.basename(file)
        dfs.append(df)
        print(f"Read {os.path.basename(file)}: {len(df)} rows")

    combined_df = pd.concat(dfs, ignore_index=True)

    # Sort by datetime
    combined_df = combined_df.sort_values('DATETIME')

    if prefer_later_contract:
        # For duplicates, keep the one with highest CONTRACT_ORDER (later contract)
        combined_df = combined_df.sort_values(['DATETIME', 'CONTRACT_ORDER'],
                                              ascending=[True, False])
    else:
        # Keep the one with lowest CONTRACT_ORDER (earlier contract)
        combined_df = combined_df.sort_values(['DATETIME', 'CONTRACT_ORDER'],
                                              ascending=[True, True])

    # Remove duplicates, keeping first occurrence based on our sorting
    combined_df = combined_df.drop_duplicates(subset=['DATETIME'], keep='first')

    # Sort by datetime again
    combined_df = combined_df.sort_values('DATETIME')
    combined_df = combined_df.reset_index(drop=True)

    # Save to CSV
    original_columns = ['DATE', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE',
                        'TICKVOL', 'VOL', 'SPREAD']

    final_df = combined_df[original_columns]
    final_df.to_csv(output_file, sep='\t', index=False)

    print(f"\nMerged file saved as: {output_file}")
    print(f"Total rows: {len(final_df)}")
    print(f"Date range: {final_df['DATE'].min()} to {final_df['DATE'].max()}")

    return combined_df


# Main execution
if __name__ == "__main__":
    # Simple merge (just remove duplicates)
    print("=" * 50)
    print("Simple merge (removing duplicates)")
    print("=" * 50)
    merged_data = merge_futures_csv_files()

    # Uncomment below if you want more control over which contract to prefer
    """
    print("\n" + "=" * 50)
    print("Merge preferring later contracts")
    print("=" * 50)
    merged_data_preferred = merge_futures_with_preference(prefer_later_contract=True)
    """