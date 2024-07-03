import pandas as pd
# import os


mt5_forex_tester5_format = True
tc2000_format = False
mt4_format = False  # False for MT5 format
mt5_daily = False    # If MT5 csv is daily
file_path = 'E:\\YandexDisk\\Desktop_Zal\\MESU24_M1_202406170000_202407031714.csv'
file_path_write = f'E:\\YandexDisk\\Desktop_Zal\\MESU24_M1_202406170000_202407031714{"w"}.csv'

if tc2000_format:
    df = pd.read_csv(file_path, parse_dates=[0], delimiter=',')  # Tab is default delimiter for MT5 files

else:
    df = pd.read_csv(file_path, parse_dates=[0], delimiter='\t')  # Tab is default delimiter for MT5 files


if tc2000_format:
    # CONVERTING TO DATETIME
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    df['Time'] = df['Date'].dt.strftime('%H:%M:%S')
    df['Date'] = df['Date'].dt.date

elif mt4_format:  # Insert column names if MT4 format
    insert_column_names = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    df.columns = insert_column_names
    df['Time'] = pd.to_datetime(df['Time'], format='mixed')
    df['Time'] = df['Time'].dt.strftime('%H:%M:%S')

elif mt5_daily:
    new_column_names = {
        '<DATE>': 'Date',
        '<TIME>': 'Time',
        '<OPEN>': 'Open',
        '<HIGH>': 'High',
        '<LOW>': 'Low',
        '<CLOSE>': 'Close',
        '<VOL>': 'Volume'
    }
    df = df.rename(columns=new_column_names)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Time'] = '00:00:00'

elif mt5_forex_tester5_format:   # Rename column names if MT5 format
    new_column_names = {
        '<DATE>': 'Date',
        '<TIME>': 'Time',
        '<OPEN>': 'Open',
        '<HIGH>': 'High',
        '<LOW>': 'Low',
        '<CLOSE>': 'Close',
        '<TICKVOL>': 'Volume'
    }
    df = df.rename(columns=new_column_names)
    df['Time'] = pd.to_datetime(df['Time'], format='mixed')
    df['Time'] = df['Time'].dt.strftime('%H:%M:%S')

# file_name = os.path.basename(file_path)
# df = df.assign(Filename=file_name)

print(df)


on_off = True      # True for write
if on_off:
    df.to_csv(file_path_write, index=False, sep=',')
else:
    pass
