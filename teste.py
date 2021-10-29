# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 04:20:22 2021

@author: DaniloDC
"""

import requests
import json
import time
import pandas as pd

coffee_shops = []
params = {}
  
endpoint_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=restaurant&location=-23.559478,-46.733533&radius=1000&region=br&type=restaurant&key=AIzaSyDeGcBJDxPtoGs1PhVVKf7PCT1jPD_iGTU"
         
res = requests.get(endpoint_url, params = params)
results =  json.loads(res.content)
coffee_shops.extend(results['results'])
time.sleep(2)
while "next_page_token" in results:
     params['pagetoken'] = results['next_page_token'],
     res = requests.get(endpoint_url, params = params)
     results = json.loads(res.content)
     coffee_shops.extend(results['results'])
     time.sleep(2)
     

Local_Nome = []
Local_Endereço = []
Local_lat = []
Local_lon = []

for i in range(len(coffee_shops)):
    
    Local = coffee_shops[i]

    try:
        Local_Nome.append(Local['name'])
    except:
        Local_Nome.append('none')
        
    try:
        Local_Endereço.append(Local['formatted_address'])
    except:
        Local_Endereço.append('none')
        
    try:
        Local_lat.append(Local['geometry']['location']['lat'])
    except:
        Local_lat.append('none')
        
    try:
        Local_lon.append(Local['geometry']['location']['lng'])
    except:
        Local_lon.append('none')
        
df_dict = {'Local_nome':Local_Nome, 'Local_Endereço':Local_Endereço, 'Local_lat':Local_lat, 'Local_lon': Local_lon}

Local_df = pd.DataFrame(df_dict)
Local_df['duplicador'] = Local_df['Local_nome'] + Local_df['Local_Endereço']

Local_df.drop_duplicates(['duplicador'], inplace=True)
Local_df.head()