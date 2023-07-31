import sys
import pandas as pd
import os
from tkinter import filedialog
from tkinter import *
from gphotospy import authorize
from gphotospy.media import Media
from gphotospy.album import Album
import datetime
import pytz
import requests
import base64

province = sys.argv[1]
# province = 'nonthaburi'
delete_day_before = 15 #day

def split_list(lst,target):
    return [lst[i:i + target] for i in range(0, len(lst), target)]

def encode_text_to_base64(text):
    try:
        text_bytes = text.encode('utf-8')
        base64_data = base64.b64encode(text_bytes).decode('utf-8')
        return base64_data
    except Exception as e:
        print(f"An error occurred: {e}")
        
def decode_base64_to_text(base64_data):
    try:
        decoded_bytes = base64.b64decode(base64_data)
        decoded_text = decoded_bytes.decode('utf-8')
        return decoded_text
    except Exception as e:
        print(f"An error occurred: {e}")

def get_id_album(province):
    album_iterator = album_manager.list()
    for a in album_iterator:
        if a['title'] == province:
            print(a['id'])
            return a['id']
    created_album = album_manager.create(province)
    id_album = created_album.get("id")
    return id_album

def upload_photos(file_names):
    album_id = [get_id_album(province)]
    if album_id:
        album_media_list = list(media_manager.search_album(album_id[0]))
        googlephoto_file = [x['filename'] for x in album_media_list]
    else:
        googlephoto_file = []
    
    must_upload = list(set(file_names) - set(googlephoto_file))

    print('must_upload=',len(must_upload),'from total=',len(file_names))

#     file_names = ['photo.png','photo2.png']
    for i,ff in enumerate(split_list(must_upload,10)):
        for ii,f in enumerate(ff):
            print(f'{i*10+ii+1}/{len(must_upload)} uploading..',f)
            media_manager.stage_media(f'photos/{f}')
        print('upload batch......................')
        media_manager.batchCreate(id_album)

def load_photofromlink(media_url):
    response = requests.get(media_url)
    downloaded_file_path = encode_text_to_base64(media_url)
    if response.status_code == 200:
        with open(f'photos/{downloaded_file_path}.png', 'wb') as f:
            f.write(response.content)


#list photo links
file_path = f'../data/df_{province}.csv'
df = pd.read_csv(file_path)
file_names = []
for index, row in df.iterrows():
    file_names.append(row['img0'])
    file_names.append(row['img1'])

#load photos from link
for i,f in enumerate(file_names):
    if f not in [decode_base64_to_text(x.split('.')[0]) for x in os.listdir('photos')]:
        try:
            print(f'{i}/{len(file_names)} loading...',f)
            load_photofromlink(f)
        except Exception as e:
            print(e)
    else:
        print(f'{i}/{len(file_names)} exist photo >',f)

#inint google photo
CLIENT_SECRET_FILE = 'client_secret_788706485156-aua909ulnbl77el0nuk3n3ahiat65sto.apps.googleusercontent.com.json'
service = authorize.init(CLIENT_SECRET_FILE)
album_manager = Album(service)
media_manager = Media(service)

id_album = get_id_album(province)

file_names = os.listdir('photos')
file_names = [x for x in file_names if '.png' in x]

#upload photos
upload_photos(file_names)

#delete old photo
album_id = [get_id_album(province)]
for aid in album_id:
    try:
        album_media_list = list(media_manager.search_album(aid))
        print('\n')
        print(aid)
        print(album_media_list)
        items = []
        for am in album_media_list:
    #         print(am['mediaMetadata']['creationTime'],type(am['mediaMetadata']['creationTime']))
            creationTime = datetime.datetime.fromisoformat(am['mediaMetadata']['creationTime'].replace("Z", "+00:00"))
            creationTime = thailand_datetime = creationTime.astimezone(pytz.timezone('Asia/Bangkok')).date()
            print(creationTime)
            if creationTime <= datetime.date.today() - datetime.timedelta(days=delete_day_before):
                print('delete',am['id'],)
                items.append(am['id'])
            
        print(aid, items)
        if items:
            album_manager.batchRemoveMediaItems(aid, items)
    except Exception as e:
        print('no photo in floder!',e)