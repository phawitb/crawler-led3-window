import pandas as pd
import os
import json
from datetime import date
import sys

# province = 'nonthaburi'
province = sys.argv[1]

def find_last_sta(sell_table):
    dates = []
    stas = []
    discount_factor = 0
    for i in sell_table.keys():
        d = sell_table[i]['date']
        a = d.split('/')
        d = str(int(a[2])-543) + a[1] + a[0]
        print(d,sell_table[i]['sta'])
        dates.append(d)
        stas.append(sell_table[i]['sta'])

        if 'ไม่มี' in sell_table[i]['sta']:
            discount_factor += 1
      
    today = date.today()
    today = today.strftime("%Y%m%d")
    
    b = [int(x)-int(today) for x in dates]
    
    idx = b.index(min([x for x in b if x > 0]))
    return dates[idx],stas[idx],dates,idx+1,discount_factor

dir_path = '../data'
res = os.listdir(dir_path)
res = [x for x in res if province in x]
res_combile = [x for x in res if 'combile' in x][0]

data_combile = json.load(open(f'../data/{res_combile}'))

DETAIL = {}
for i,k in enumerate(data_combile.keys()):
#     print(data_combile[k])
    D = {}
    columns = ['sell_order','case_id','deed_number','type','size0','size1','size2','tumbon','aumper','province','pay_down','status','max_price']
    for c in columns:
        try:
            D[c] = data_combile[k]['data'][c]
        except:
            D[c] = None
    
    if 'sell_table' in data_combile[k]['data'].keys():
        D['lastSta_date'], D['lastSta_detail'],D['bid_dates'],D['bid_time'],D['discount_factor'] = find_last_sta(data_combile[k]['data']['sell_table'])
        
        if D['discount_factor'] > 3:
            D['discount_factor'] = 3

        D['current_price'] = int(D['max_price']*(1-D['discount_factor']*0.1))
        
    if 'gps_data' in data_combile[k]['data'].keys():
        for d in data_combile[k]['data']['gps_data'].keys():
            if data_combile[k]['data']['gps_data'][d]['gps']:
                D['lat'] = data_combile[k]['data']['gps_data'][d]['gps'].split(',')[0]
                D['lon'] = data_combile[k]['data']['gps_data'][d]['gps'].split(',')[1]
                break
                
    if 'img' in data_combile[k]['data'].keys():
#         print(data_combile[k]['data']['img'])
        for ii in range(len(data_combile[k]['data']['img'])):
            D[f'img{ii}'] = data_combile[k]['data']['img'][ii]
        
    D['link'] = data_combile[k]['link']
    DETAIL[i] = D
    print(i,D)
    print('-'*20)
        
df = pd.DataFrame(DETAIL)
df = df.transpose()

df.to_csv(f"../data/df_{province}.csv", index = False)