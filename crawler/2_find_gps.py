from webdriver_manager.chrome import ChromeDriverManager   #-------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import json
from dateutil.relativedelta import *
import os
from selenium.webdriver.support.ui import Select
import configure
import sys
import csv
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import requests

time.sleep(10)

TOKEN_GROUP_ALL = '1hZqXJ1UwUlSD2eIIMjnobPb5PkoQIKT70Y0IR5SAzt'

def line_noti(token,msg):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
    r = requests.post(url, headers=headers, data = {'message':msg})
    return r.text

def scrolling_down(t):
    for i in range(t):
        driver.execute_script("window.scrollBy(0,2000)","")
        time.sleep(0.5)
        
def get_text(x):
    return driver.find_element(By.XPATH,x).text

def get_herf(x):
    attb = ['href','onclick','src']
    for a in attb:
        v = driver.find_element(By.XPATH,x).get_attribute(a)
        if v:
            break 
    return v

def click(x):
    driver.find_element(By.XPATH,x).click()
    
def sent_key(x,val):
    driver.find_element(By.XPATH, x).send_keys(val)
    
def clear(x):
    driver.find_element(By.XPATH, x).clear()
    

def select_scroll(x,val):
    #     x = '/html/body/nav/form[1]/div/select'
        element= Select(driver.find_element(By.XPATH,x))
        element.select_by_visible_text(val)   # ddelement.select_by_value('12')
        
def list_aumphers(province):
    provinces = get_text('/html/body/nav/form[1]/div/select').split('\n')[1:]
    aumphers = []
    if province in provinces:
        select_scroll('/html/body/nav/form[1]/div/select',province)
        aumphers = get_text('/html/body/nav/form[2]/div/select').split('\n')[1:]
    return aumphers
        
def find_gps(thai_province,aumper,deed_no):
    def read_box():
        data = {}
        L = ['deed_id','page_explor','land_id','position','tumbon','aumpher','province','area','eva_price','gps']
        for i,l in enumerate(L):
            
            # driver.implicitly_wait(10)
            start = time.time()
            d = None
            while not d and time.time()-start < 10:
                d = get_text(f'/html/body/div[1]/div[3]/span/div/div[2]/div[2]/div/div[2]/div[{i+1}]/div[2]')
#                 print(d)
                data[l] = d

        return data
    
    # print('\n\n\nx',x)
#     print('aumper',aumper)
#     aums = [x for x in aumphers if aumper in x]
#     print('aums',aums)
    
    # aumper = 'บางกรวย'
#     aumper = 'บางกรวย (บางใหญ่)บางกรวย'

    if thai_province == 'กรุงเทพฯ':
        thai_province = 'กรุงเทพมหานคร'
    if '(' in aumper:
        aumper = aumper.replace('(',' ').replace(')','').split()
    else:
        aumper = [aumper]
    aumper = [x.strip() for x in aumper]
#     print('aumper',aumper)

    if thai_province not in aumphers.keys():
        aumphers[thai_province] = list_aumphers(thai_province)
        
#     print('aumphers[thai_province] ',aumphers[thai_province] )

    aums = []
    for a in aumper:
        aums += [x for x in aumphers[thai_province] if a in x]
    #     aums += 
    print('aums',aums)

    for aumper in aums:
        print(thai_province,aumper)
        try:
            select_scroll('/html/body/nav/form[1]/div/select',thai_province)
            select_scroll('/html/body/nav/form[2]/div/select',aumper)

            clear('/html/body/nav/form[3]/span/input')
            sent_key('/html/body/nav/form[3]/span/input',deed_no)

            click('/html/body/nav/form[4]/button')
            time.sleep(2)
            box = read_box()
        #     click('/html/body/div[1]/div[3]/span/div/div[1]/button')
            return box
        except Exception as e:
            print('e',e)
            # pass
    return None

def find_exist_gps(id):
    try:
        with open(f'../data/{province}_gps_data.json', 'r') as openfile:
            gps_data = json.load(openfile)
    except:
        gps_data = {}

    if id in gps_data.keys():
        return gps_data[id]

# province = 'nonthaburi'
# find_exist_gps('30715')

#---------------------------------------------------------------
# province = 'nonthaburi'
province = sys.argv[1]

line_noti(TOKEN_GROUP_ALL,f'process2 findGPS start!--->{province}')

thai_province = configure.search_province[province][0]
chrome_headless = configure.chrome_headless

options = webdriver.ChromeOptions()
if chrome_headless:
    options.add_argument("headless")
# options.add_argument('window-size=800x600')
options.add_argument('window-size=1920x1080')
# driver = webdriver.Chrome(ChromeDriverManager(version=configure.chrome_version).install(),chrome_options=options)   #-----------------
driver = webdriver.Chrome(service=Service(executable_path="chromedriver"), options=options)
# driver.maximize_window()
print('driver.get_window_size()',driver.get_window_size())

driver.get('https://landsmaps.dol.go.th/')

try:
    # u = '/html/body/div[25]/div/div/div/div[1]/button/i'
    u = '/html/body/div[25]/div/div/div/div[3]/button'
    element_order = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH,u)))
    # time.sleep()
    # driver.find_element(By.XPATH,u).click()
    time.sleep(10)
    click(u)
except:
    pass


# time.sleep(10)
# try:
#     click(u)
# except:
#     pass
aumphers = {}
aumphers[thai_province] = list_aumphers(thai_province)
print('aumphers',aumphers)

with open(f'../data/{province}_led.json', 'r') as openfile:
    data = json.load(openfile)
try:
    with open(f'../data/{province}_gps_data.json', 'r') as openfile:
        gps_data = json.load(openfile)
except:
    gps_data = {}
exist_gps = gps_data.keys()
# data

line_noti(TOKEN_GROUP_ALL,f'All deed ---> {len(list(data.keys()))}')

for i,k in enumerate(data.keys()):
    if i%30 == 0:
        line_noti(TOKEN_GROUP_ALL,f'Progress findGPS -->{i}/{len(list(data.keys()))}')

    if 'deed_number' in data[k].keys():
        deed = data[k]['deed_number'].split(',')
        deed = [x.strip('-') for x in deed]
        print('\n\n\n',deed,type(deed))
        # extrack range deed number
        X = []
        for x in deed:
            if '-' in x:
                a = int(x.split('-')[0])
                b = int(x.split('-')[1])
                X += list(range(a,b+1))
                # print(list(range(a,b+1)))
            else:
                X.append(x)
        deed = X

        print(deed,type(deed))
        for d in deed:
            print(d)
            if d in exist_gps:
                print('exist gps')
            else:
    #             print('not exist gps',province,d,data[p]['data']['aumper'])
                thai_province = data[k]['province'].strip()
                aumper = data[k]['aumper']
                print(d,'thai_province',thai_province,'aumper',aumper)
                a = find_gps(thai_province,aumper,d)
                if a:
                    line_noti(TOKEN_GROUP_ALL,f'find GPS from website,{a}')
                    print(f'find GPS from website,{a}')
                    gps_data[str(d)] = a
                    with open(f"../data/{province}_gps_data.json", "w") as outfile:
                        outfile.write(json.dumps(gps_data, indent=4))
                else:
                    print('Not find gps from website',a)
                    line_noti(TOKEN_GROUP_ALL,f'Not find gps from website,{a}')
    else:
        line_noti(TOKEN_GROUP_ALL,f'Not have deed number {k}')

        
line_noti(TOKEN_GROUP_ALL,f'Finish process2')
