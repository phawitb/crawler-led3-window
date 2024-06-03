# C:\Users\phawit\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
import subprocess
import csv
import requests
import pandas as pd
import os

TOKEN_GROUP_ALL = '1hZqXJ1UwUlSD2eIIMjnobPb5PkoQIKT70Y0IR5SAzt'

def get_crawlerstatus():
    with open('../data/stage.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            return row[0].split('/')

def order_province(PROVINCE):
    file_path = '../data/currentstatus.csv'

    df = pd.read_csv(file_path)

    df[['is', 'gps']] = df['isgps'].str.split('/', expand=True)
    df['total'] = df['total'].astype(str)
    df = df[df['total'] == df['gps']]
    df = df.sort_values(by='date', ascending=False)

    unique_list = []
    for item in list(df['province']):
        if item not in unique_list:
            unique_list.append(item)
    unique_list = unique_list[::-1]

    cp = []
    for p in unique_list:
        if p in PROVINCE:
            cp.append(p)

    return list(set(PROVINCE)-set(cp)) + cp

def line_noti(token,msg):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
    r = requests.post(url, headers=headers, data = {'message':msg})
    return r.text

def process1_staus():
    with open('../data/stage.csv', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        process1_staus = next(csv_reader)[0]
        print(process1_staus)
    return process1_staus == 'True'

def run_other_script_with_args(script_path, arg):
    subprocess.run(["python", script_path] + [arg])
    
PROVINCE = ['nakhonpathom','lopburi','nonthaburi','samutsakorn','chonburi','songkhla','nokhonnayok','ratchaburi','bangkok','phuket','chiangmai','lampang','lumphun','pathumthani']
PROVINCE = order_province(PROVINCE)

line_noti(TOKEN_GROUP_ALL,'v2window sever start!')

# for province in PROVINCE:
#     run_other_script_with_args('5_upload2sheet.py',province)
#     line_noti(TOKEN_GROUP_ALL,f'5_upload2sheet.py {province}')

#update chrome driver
# subprocess.run(["python", '0_update_chromedriver.py'])

#update lastSta
subprocess.run(["python", '0_update_lastSta.py'])
for p in [x.replace('.csv','').split('df_')[1] for x in os.listdir("../data") if 'df_' in x]:
    run_other_script_with_args('4_upload2github.py',p)
    line_noti(TOKEN_GROUP_ALL,f'update laststa--> {p}')

#crawler loop
for province in PROVINCE:

    ready = False

    for i in range(10):
        run_other_script_with_args('1_crawler_led.py',province)
        cs = get_crawlerstatus()
        line_noti(TOKEN_GROUP_ALL,f'[{i}]==1_crawler_led.py {province}')

        if cs:
            ready = True
            break;
    
    # for i in range(10):
    #     cs = get_crawlerstatus()
    #     print('cs----------',cs)
    #     if cs[0] != cs[1]:
    #         run_other_script_with_args('1_crawler_led.py',province)
    #         line_noti(TOKEN_GROUP_ALL,f'attemp{i+2}: 1_crawler_led.py {province}')
    #     else:
    #         ready = True
    #         # break

    # if process1_staus():
    if ready:
    # if True:

        # try:
        #     run_other_script_with_args('5_upload_googlephoto.py',province)
        #     line_noti(TOKEN_GROUP_ALL,f'5_upload_googlephoto.py {province}')
        # except Exception as e:
        #     line_noti(TOKEN_GROUP_ALL,f'Error!!! 5_upload_googlephoto.py {province} {e}')
        #     pass
        
        run_other_script_with_args('2_find_gps.py',province)
        line_noti(TOKEN_GROUP_ALL,f'2_find_gps.py {province}')

        run_other_script_with_args('2_find_gps.py',province)
        line_noti(TOKEN_GROUP_ALL,f'2_find_gps.py {province}')

        run_other_script_with_args('3_data2csv.py',province)
        line_noti(TOKEN_GROUP_ALL,f'3_data2csv.py {province}')

        run_other_script_with_args('4_upload2github.py',province)
        line_noti(TOKEN_GROUP_ALL,f'4_upload2github.py {province}')

        

        

        


        



