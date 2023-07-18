import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import requests
import io
from streamlit_folium import st_folium
from datetime import datetime



COLORS = {
    'ที่ดินพร้อมสิ่งปลูกสร้าง' : 'red',
    'ที่ดินว่างเปล่า' : 'green',
    'ห้องชุด' : 'blue',
    'หุ้น' : 'gray'
}

if "current_id" not in st.session_state:
    st.session_state["current_id"] = 0
if "df" not in st.session_state:
    st.session_state["df"] = pd.DataFrame()
if "stage" not in st.session_state:
    st.session_state["stage"] = 0

def get_pos(lat,lng):
    return lat,lng

def get_data(province):
    # province = 'nonthaburi'
    url = f'https://raw.githubusercontent.com/phawitb/crawler-led3-window/main/df_{province}.csv'
    response = requests.get(url)
    df = pd.read_csv(io.StringIO(response.text))
    return df




def create_map(df):
    #init map
    initial_location = [13.9162258,100.3809889]  # New York City coordinates
    map = folium.Map(location=initial_location, zoom_start=12)

    # L = ['A','B','C']
    L = list(df['type'].unique())
    # L.sort()

    # print('LLLL',L)
    # ['ที่ดินพร้อมสิ่งปลูกสร้าง', 'ที่ดินว่างเปล่า', 'หุ้น', 'ห้องชุด']
    Layers = []
    for l in L:
        la = folium.FeatureGroup(name=l)
        map.add_child(la)

        Layers.append(la)

    for index, row in df.iterrows():
        # print("row['size0']",row['size0'],type(row['size0']))
        # print('imgggggggg',str(row['img0']))

        color = COLORS[row['type']]
        fill_color = COLORS[row['type']]
        if row['size0'] < 30 and row['size1'] == 0 and row['size2'] == 0 and row['type']=='ที่ดินพร้อมสิ่งปลูกสร้าง':
            color = 'orange'
            fill_color = 'orange'




        if str(row['img0']) == 'nan':
            fill_opacity = 0.3
            fill_color = 'black'
            # print('bbbbbbbbbb')
        else:
            fill_opacity = 0.8
            # fill_color = COLORS[row['type']]
        if str(row['lon']) != 'nan':
            # print(row['lat'], row['lon'],row['img0'])
            # max_price,lastSta_date,lastSta_detail
            A = ''
            if row['size2'] != 0:
                A += f"{row['size2']} ไร่ "
            if row['size1'] != 0 or row['size2']>0:
                A += f"{row['size1']} งาน "
            if row['size0'] != 0 or row['size2']>0 or row['size1']>0:
                A += f"{row['size0']} ตร.ว."

            popup=folium.Popup(f"""<h2>{row['type']}</h2>
              <h5>{row['tumbon']},{row['aumper']},{row['province']}</h5>
              <h5>{A}</h5>
              <h5>นัด{int(row['bid_time'])} : {datetime.strptime(str(int(row['lastSta_date'])), "%Y%m%d").strftime("%d/%m/%Y")} {row['lastSta_detail']}</h5>
              <h5>{row['status']}</h5>
              <h4><a href="{row['link']}" target="_blank">{'{:,}'.format(int(row['max_price']))}</a></h4>
              <img src="{row['img0']}" alt="Trulli" style="max-width:100%;max-height:100%">""", max_width=400)
            marker = folium.Circle(popup=popup,location=[float(row['lat']), float(row['lon'])], radius=100,weight=1, fill=True, color=color,fill_color=fill_color,fill_opacity=fill_opacity)

# date_string = 
# datetime.strptime(str(int(row['lastSta_date'])), "%Y%m%d").strftime("%Y-%m-%d")

# {'{:,}'.format(int(row['max_price']))}
    #         color='blue',
    # fill=True,
    # fill_color='blue',
    # fill_opacity=0.4,


            # marker = folium.Marker(location=[float(row['lat']), float(row['lon'])], popup=row['max_price'],icon=folium.Icon(color=COLORS[row['type']]))
            # marker = folium.Circle(popup=row['max_price'],location=[float(row['lat']), float(row['lon'])], radius=5, fill=True, color=COLORS[row['type']])

            i = L.index(row['type'])
            marker.add_to(Layers[i])




    satellite_tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    folium.TileLayer(tiles=satellite_tiles, attr="Esri World Imagery", name="Satellite").add_to(map)
    # folium.TileLayer(tiles='Stamen Terrain',name="Satellite2").add_to(map)
    folium.LayerControl().add_to(map)

    return map

def filter_equal(df,col,L):
    df2 = df[df[col]==L[0]]
    for a in L[1:]:
        df2 = df2._append(df[df[col]==a])
    return df2

def filter_range(df,col,mi,mx):
    df['max_price'].fillna(-1, inplace = True)
    df2 = df[df[col]>mi]
    df2 = df2[df2[col]<mx]
    return df2

def strprice2int(s):
    if 'k' in s or 'M' in s:
        if s[-1] == 'k':
            x = 1000
        if s[-1] == 'M':
            x = 1000000
        return int(s[:-1])*x
    else:
        return int(s)

def filter_df(df,selected_province,selected_aumpher,selected_min,selected_max,selected_date,types,size_min, size_max):
    print('selectttt',selected_province,selected_aumpher,selected_min, selected_max,selected_date,types,size_min, size_max)

    df['tarangwa'] = df['size0']+df['size1']*100+df['size2']*400

    if size_min != 'max':
        size_min = int(size_min)
    else:
        size_min = 10000
    if size_max != 'max':
        size_max = int(size_max)
    else:
        size_max = 100000
    df = filter_range(df,'tarangwa',size_min,size_max)


    T = []
    for t in types.keys():
        if types[t]:
            T.append(t)
    #filter df
    if not selected_aumpher:
        selected_aumpher = list(df['aumper'].unique())
    selected_date = selected_date.replace('/','')
    dfs = filter_equal(df,'aumper',selected_aumpher)
    dfs = filter_range(dfs,'max_price',strprice2int(selected_min),strprice2int(selected_max))
    dfs = filter_equal(dfs,'type',T)
    if selected_date != 'All Date':
        matchDate = []
        for index, row in dfs.iterrows():
            if selected_date in eval(row['bid_dates']):
                matchDate.append(True)
            else:
                matchDate.append(False)
        dfs['matchDate'] = matchDate
    else:
        dfs['matchDate'] = True
    dfs = dfs[dfs['matchDate'] == True]
    return dfs

def main():
    
    
    st.set_page_config(layout="wide")
    st.markdown(
    """
    <style>
    .css-1aumxhk {
        padding: 0;
        border: none;
        box-shadow: none;
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    st.sidebar.header("Find")
    selected_province = st.sidebar.selectbox('Province',['Select Province','nonthaburi', 'bangkok'])
    if selected_province != 'Select Province':
        df = get_data(selected_province)
        selected_aumpher = st.sidebar.multiselect('Aumpher',list(df['aumper'].unique()))
        selected_min, selected_max = st.sidebar.select_slider('Price',options=['0','100k','500k','1M','3M','5M','10M','500M'],value=('0', '500M'))

        #find all dates
        all_date = []
        for i in list(df['bid_dates'].unique()):
            # print(i,type(i))
            if str(i) != 'nan':
                all_date = all_date+eval(i)
        all_date = set(all_date)
        all_date = ['All Date'] + [datetime.strptime(x, '%Y%m%d').strftime('%Y/%m/%d') for x in all_date]
        selected_date = st.sidebar.selectbox('Date',all_date)


        # L = list(df['type'].unique())
        types = {}
        for l in list(df['type'].unique()):
            types[l] = st.sidebar.checkbox(l,value=True)

        size_min, size_max = st.sidebar.select_slider('Size(ตร.ว.)',options=['0','20','30','40','50','100','200','400','max'],value=('0', 'max'))
        print('size_min, size_max',size_min, size_max)


            

        print('types',types)
        # selected_date = st.sidebar.selectbox('Date',('all', '06/06/2023', '09/06/2023','12/06/2023'))
        if st.sidebar.button('🌎 Map'):
            st.session_state["stage"] = 1
            dfs = filter_df(df,selected_province,selected_aumpher,selected_min,selected_max,selected_date,types,size_min, size_max)


            map = create_map(dfs)
            # map.get_root().html.add_child(folium.Element('<style>#map-container { height: 100vh !important; width: 100% !important; }</style>'))
            m = folium_static(map,height=1000, width=1800)

        if st.sidebar.button('🏠 Order-ID'):
            st.session_state["stage"] = 2
            dfs = filter_df(df,selected_province,selected_aumpher,selected_min,selected_max,selected_date,types,size_min, size_max)
            dfs = dfs.reset_index(drop=True)
            st.session_state["df"] = dfs
            # dfs
            
        # tab1, tab2 = st.tabs(["Map", "Order-ID"])
        if st.session_state["stage"] == 2:
            col1, col2 = st.columns([3,2])
            b1, b2 = col1.columns([1,6])
            if st.session_state["df"].shape[0] > 0:
                with b1:
                    if st.button('⬅️ Previous'):
                        if st.session_state["current_id"] > 0:
                            st.session_state["current_id"] -= 1
                with b2:
                    if st.button('Next ➡️'):
                        if st.session_state["current_id"] < st.session_state["df"].shape[0]:
                            st.session_state["current_id"] += 1

                # st.session_state["df"]
                r = st.session_state["df"].iloc[st.session_state["current_id"]]

                
                col11, col12 = col1.columns(2)
                with col11:
                    if 'ปลอด' in r['status']:
                        color = 'green'
                    else:
                        color = 'red'
                    A = ''
                    if r['size2'] != 0:
                        A += f"{r['size2']} ไร่ "
                    if r['size1'] != 0 or r['size2']>0:
                        A += f"{r['size1']} งาน "
                    if r['size0'] != 0 or r['size2']>0 or r['size1']>0:
                        A += f"{r['size0']} ตร.ว."

                    st.header(f"""# {st.session_state["current_id"]+1}/{st.session_state["df"].shape[0]}({r['sell_order']} {r['type']})""")
                    st.subheader(f"{r['tumbon']},{r['aumper']},{r['province']}")
                    st.subheader(f":red[{A}]")
                    st.subheader(f"""นัด {int(r['bid_time'])} : {datetime.strptime(str(int(r['lastSta_date'])), "%Y%m%d").strftime("%d/%m/%Y")} {r['lastSta_detail']}""")
                    st.subheader(f":{color}[{r['status']}]")
                    st.subheader(f":{color}[วางเงิน {'{:,}'.format(int(r['pay_down']))}]")
                    st.header(f"[:blue[฿ {'{:,}'.format(int(r['max_price']))}]]({r['link']})")

                col111, col112 = col1.columns(2)
                with col111:
                    st.image(r['img0'], width = 400)

                with col112:
                    st.image(r['img1'], width = 400)

                with col2:
                    map2 = folium.Map(location=[r['lat'], r['lon']], zoom_start=16)

                    # popup=folium.Popup(f"""<h2>{r['type']}</h2>
                    #     <h5>{r['tumbon']},{r['aumper']},{r['province']}</h5>
                    #     <h5>{A}</h5>
                    #     <h5>นัด{int(r['bid_time'])} : {datetime.strptime(str(int(r['lastSta_date'])), "%Y%m%d").strftime("%d/%m/%Y")} {r['lastSta_detail']}</h5>
                    #     <h5>{r['status']}</h5>
                    #     <h4><a href="{r['link']}" target="_blank">{'{:,}'.format(int(r['max_price']))}</a></h4>""", max_width=400)


                    folium.Marker(
                        [r['lat'], r['lon']]  #, popup=popup, tooltip='aaaa'
                    ).add_to(map2)

                    satellite_tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
                    folium.TileLayer(tiles=satellite_tiles, attr="Esri World Imagery", name="Satellite").add_to(map2)
                    # folium.TileLayer(tiles='Stamen Terrain',name="Satellite2").add_to(map)
                    folium.LayerControl().add_to(map2)

                    # call to render Folium map in Streamlit
                    st_data2 = st_folium(map2, width=725,height=900)
                    # st_data2


if __name__ == '__main__':
    main()


