import subprocess
import csv
import requests

TOKEN_GROUP_ALL = '1hZqXJ1UwUlSD2eIIMjnobPb5PkoQIKT70Y0IR5SAzt'

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
    
PROVINCE = ['nonthaburi','nakhonpathom','samutsakorn','chonburi','songkhla']

line_noti(TOKEN_GROUP_ALL,'window sever start!')

for province in PROVINCE:

    run_other_script_with_args('1_crawler_led.py',province)
    line_noti(TOKEN_GROUP_ALL,f'1_crawler_led.py {province}')
    run_other_script_with_args('1_crawler_led.py',province)
    line_noti(TOKEN_GROUP_ALL,f'1_crawler_led.py {province}')
    if process1_staus():
        run_other_script_with_args('2_find_gps.py',province)
        line_noti(TOKEN_GROUP_ALL,f'2_find_gps.py {province}')

        run_other_script_with_args('2_find_gps.py',province)
        line_noti(TOKEN_GROUP_ALL,f'2_find_gps.py {province}')

        run_other_script_with_args('3_combile_data.py',province)
        line_noti(TOKEN_GROUP_ALL,f'3_combile_data.py {province}')

        run_other_script_with_args('4_data2csv.py',province)
        line_noti(TOKEN_GROUP_ALL,f'4_data2csv.py {province}')

        run_other_script_with_args('5_upload2sheet.py',province)
        line_noti(TOKEN_GROUP_ALL,f'5_upload2sheet.py {province}')

        run_other_script_with_args('5_upload2github.py',province)
        line_noti(TOKEN_GROUP_ALL,f'5_upload2github.py {province}')

        run_other_script_with_args('5_upload_googlephoto.py',province)
        line_noti(TOKEN_GROUP_ALL,f'5_upload_googlephoto.py {province}')

        


        



