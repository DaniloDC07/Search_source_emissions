# -*- coding: utf-8 -*-
"""
@author: DaniloDC

Criar uma formar de salvar o dataframe em um arquivo à cada chamada.

"""

import requests
import json
import time
import pandas as pd

def main():
    # Elaboração do dicionario de palavras
    
    words = ['Aterros+Sanitarios',
             'Industrias',
             'Crematorios',
             'Depositos+de+lixo',
             'Industrias',
             'Termeletricas',
             'Usinas']
    
    String_search = ''
    bol = False
    while String_search == '':
        String_search = input("Entre com o objeto de pesquisa, com a letra inical maiuscula, sem acentos e com espaços indicados por '+': " )
        bol = string_busca(words, String_search)
        if bol == False or len(String_search) <= 3:
            String_search = ''
            print(f"\n\
    Error: Indicar ao menos um dos seguintes objetos \n\
                  \n\
    {words}")
    
    
    # Localização
    Latitude = float(input("Entre com a latitude do local central: "))
    Longitude = float(input("Entre com a longitude do local central: "))
    Lat_Long = f'{Latitude},{Longitude}'
    
    
    # Raio
    raio = 0
    while raio == 0:
        raio = int(input("Entre com o raio em metros: "))
        if raio < 0:
            raio = 0
            print("\n\
    Error: Valor negativo \n\
                  \n\
    Favor indicar um valor maior ou igual a zero")
    
    
    # URL e API Google
    List_itens = []
    params = {}
      
    endpoint_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={String_search}&location={Lat_Long}&radius={raio}&region=br&key=AIzaSyDeGcBJDxPtoGs1PhVVKf7PCT1jPD_iGTU" 

    res = requests.get(endpoint_url, params = params)
    results =  json.loads(res.content)
    List_itens.extend(results['results'])
    time.sleep(2)
    while "next_page_token" in results:
         params['pagetoken'] = results['next_page_token'],
         res = requests.get(endpoint_url, params = params)
         results = json.loads(res.content)
         List_itens.extend(results['results'])
         time.sleep(2)
    
    # Lista de cada informação para agrupar no dataframe
    Local_Nome = []
    Local_Endereço = []
    Local_lat = []
    Local_lon = []
    
    for i in range(len(List_itens)):
        Local = List_itens[i]
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
            
    # DataFrame com as informações dos locais procurados 
    df_dict = {'Local_nome':Local_Nome, 'Local_Endereço':Local_Endereço, 'Local_lat':Local_lat, 'Local_lon': Local_lon}
    Local_df = pd.DataFrame(df_dict)
    # Removendo locais duplicados
    Local_df['duplicador'] = Local_df['Local_nome'] + Local_df['Local_Endereço']
    Local_df.drop_duplicates(['duplicador'], inplace=True)
    

# Funções auxiliares
def string_busca(lista, palavra):
    bol = False
    i = 0
    while bol == False and i < len(lista):
        if palavra in lista[i]:
            bol = True
        i += 1
    return bol

main()