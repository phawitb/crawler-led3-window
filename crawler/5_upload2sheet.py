import ezsheets
import time
import sys
import pandas as pd
import math
from datetime import datetime
import ast
import numpy as np
import configure

province = sys.argv[1]

def tranDate(input_date_str):
    input_date_obj = datetime.strptime(input_date_str, "%Y%m%d")
    formatted_date_str = input_date_obj.strftime("%m/%d/%Y")
    return formatted_date_str

df = pd.read_csv(f'../data/df_{province}.csv')

#change date to usa format
L_lastSta_date = []
L_bid_dates = []
for index, row in df.iterrows():
    if not math.isnan(row['lastSta_date']):
        lastSta_date = tranDate(str(int(row['lastSta_date'])))
        bid_dates = [tranDate(x) for x in ast.literal_eval(row['bid_dates'])]
    else:
        lastSta_date = None
        bid_dates = None
    L_lastSta_date.append(lastSta_date)
    L_bid_dates.append(str(bid_dates))
df['lastSta_date'] = L_lastSta_date
df['bid_dates'] = L_bid_dates

df = df.replace(np.nan, None)

#updode to sheet
# data_list = df.values.tolist()
data_list = [df.columns.tolist()] + df.values.tolist()

L = ezsheets.listSpreadsheets()
if f'led-data' in [L[x] for x in L]:
    print(f'led-data exist')
    spreadsheet = ezsheets.Spreadsheet(f'led-data')
    sheet = spreadsheet[f'Sheet{configure.search_province[province][2]}']
else:
    print(f'led-data not exist > create new file')
    spreadsheet = ezsheets.createSpreadsheet(f'led-data')
    sheet = spreadsheet[f'Sheet{configure.search_province[province][2]}'] # Get the first sheet in the spreadsheet

sheet.updateRows(data_list)
print('Update comlete!!')

