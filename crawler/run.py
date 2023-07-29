import subprocess
import csv

def process1_staus():
    with open('../data/stage.csv', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        process1_staus = next(csv_reader)[0]
        print(process1_staus)
    return process1_staus == 'True'

def run_other_script_with_args(script_path, arg):
    subprocess.run(["python", script_path] + [arg])
    
PROVINCE = ['nonthaburi','nakhonpathom','samutsakorn','chonburi','songkhla']

for province in PROVINCE:

    run_other_script_with_args('1_crawler_led.py',province)
    run_other_script_with_args('1_crawler_led.py',province)
    if process1_staus():
        run_other_script_with_args('2_find_gps.py',province)
        run_other_script_with_args('2_find_gps.py',province)
        run_other_script_with_args('3_combile_data.py',province)
        run_other_script_with_args('4_data2csv.py',province)
        run_other_script_with_args('5_upload2sheet.py',province)



