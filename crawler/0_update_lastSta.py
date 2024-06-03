import os
import pandas as pd
from datetime import datetime,date
# import json
import ast

def find_last_sta(sell_table):
    dates = []
    stas = []
    discount_factor = 0
    for i in sell_table.keys():
        d = sell_table[i]['date']
        a = d.split('/')
        d = str(int(a[2])-543) + a[1] + a[0]
        # print(d,sell_table[i]['sta'])
        dates.append(d)
        stas.append(sell_table[i]['sta'])

        if 'ไม่มี' in sell_table[i]['sta']:
            discount_factor += 1
      
    today = date.today()
    today = today.strftime("%Y%m%d")
    
    b = [int(x)-int(today) for x in dates]
    
    # print(dates)
    # print(b)
    try:
        idx = b.index(min([x for x in b if x >= 0]))
    except:
        idx = b.index(max(b))
    return dates[idx],stas[idx],dates,idx+1,discount_factor

directory_path = "../data"
files = os.listdir(directory_path)

df_files = [x for x in files if 'df_' in x]
print(df_files)


# df_file = df_files[0]
for df_file in df_files:
    df = pd.read_csv(f'../data/{df_file}')
    print(df)
    for index, row in df.iterrows():
        print('\n\nxxxx',row['sell_table'],type(row['sell_table']))
        if str(row['sell_table']) != 'nan':
            data_dict = ast.literal_eval(row['sell_table'])
            print('data_dict',data_dict)
            D = {}
            D['lastSta_date'], D['lastSta_detail'],D['bid_dates'],D['bid_time'],D['discount_factor'] = find_last_sta(data_dict)
            if 'max_price' in D.keys():
                if D['discount_factor'] > 3:
                    D['discount_factor'] = 3
                D['current_price'] = int(D['max_price']*(1-D['discount_factor']*0.1))

            for k in D.keys():
                df.at[index, k] = D[k]

    df.to_csv(f'../data/{df_file}', index=False)







# for file in files:
#     print(file)
