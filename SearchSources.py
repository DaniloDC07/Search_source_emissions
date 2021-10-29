# -*- coding: utf-8 -*-
"""
@author: DaniloDC

Criar uma formar de salvar o dataframe em um arquivo à cada chamada.

"""

import requests
import json
import time
import pandas as pd
import pickle
import sys
import os


class SearchSources:
    '''
        -------------------------------------------------------------------------------------------------------------------------------  
        Parameters
            
        text:
            String com inicial maiscula, sem acentos e com espaços indicados por '+', designa o objeto de pesquisa
        lat: 
            Latitude, float     
        long: 
            Longitude, float
        radius: 
            Raio a partir do centro (lat, long), float positivo
        APIKey:
            API Key Google, para obter uma chave acesse: https://console.cloud.google.com/home
        -------------------------------------------------------------------------------------------------------------------------------   
        Attributes
        
        self.text:
            Retorna uma string do objeto de pesquisa dado
            
        self.coord:
            Retorna uma tupla com a latitude e longitude dados
            
        self.radius:
            Retorna o raio dado
            
        self.key:
            Retorna a API Key
            
        self.wordbank:
            Retorna uma lista com o banco de palavras disponivel
            
        self.cache
            Retorna um dicionario com as ultimas buscas realizadas e seus respectivos resultados
        -------------------------------------------------------------------------------------------------------------------------------
        Functions
        
        save_df(self):
            Salva um dataframe.csv com as informações do Nome, Endereço, Latitude, Longitude e o Tipo dos objetos listados na pesquisa
            
        save_cache(self, Nome):    
            Salva um conjunto de dataframes correspondentes a pesquisas realizadas anteriormente e armazenadas
        -------------------------------------------------------------------------------------------------------------------------------
        '''
        
    def __init__(self, text = None, lat = 0, long = 0, radius = 0, APIKey = None):
        
        try:
            arq = open('ss_cache_(dont delete).bin', "rb")
        except:
            arq = open('ss_cache_(dont delete).bin', "wb") # Cria um arquivo novo
            arq.close()
            arq = open('ss_cache_(dont delete).bin', "rb") # Ler o arquivo
    
        if os.stat(arq).st_size == 0:
            self.cache = {}
        else:
            self.cache = pickle.load(arq)
        arq.close()
        
        self.text = text
        self.coord = (lat, long)
        self.radius = radius
        self.key = APIKey
        self.wordbank = sorted(['Aterros+Sanitarios',
             'Industrias',
             'Crematorios',
             'Depositos+de+lixo',
             'Industrias',
             'Termeletricas',
             'Usinas'])
        self.key = APIKey
        self.cache = {}
        
        if self.text == None or self.text == '' or len(self.text) <= 3:
            bol = False
        else:
            bol = True
        if bol == False:
            self.text = None
            print(f"\n\
\033[1;31;mError:\033[0m Tente novamente, mas indicando ao menos um dos seguintes objeto com a letra inical maiuscula, sem acentos e com espaços indicados por '+': \n\
                      \n")
            printa(self.wordbank)
            sys.exit()

        if self.radius < 0:
            self.radius = None
            print("\n\
\033[1;31;mError:\033[0m Raio com Valor negativo \n\
    Favor indicar um valor maior ou igual a zero \n")
            sys.exit()
    
        # Se o objeto pesquisado não estiver no cache, executar:
        if bol == True and self.text not in self.cache:
            # URL e API Google
            List_itens = []
            params = {}
              
            endpoint_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={self.text}&location={str(lat)},{str(long)}&radius={radius}&region=br&key={APIKey}" 
        
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
            Local_Types = []
            
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
                try:
                    Local_Types.append(Local['types'])
                except:
                    Local_Types.append('none')
                    
            # DataFrame com as informações dos locais procurados 
            df_dict = {'Nome':Local_Nome, 'Endereço':Local_Endereço, 'Latitude':Local_lat, 'Longitude': Local_lon, 'Tipos': Local_Types}
            Local_df = pd.DataFrame(df_dict)
            # Removendo locais duplicados
            Local_df['duplicador'] = Local_df['Nome'] + Local_df['Endereço']
            Local_df.drop_duplicates(['duplicador'], inplace=True)
            
            self.df = Local_df
            self.cache[self.text] = self.df
            
            # Salvando escrevendo no arquivo cache
            arq = open('ss_cache_(dont delete).bin', "wb")
            pickle.dump(self.cache,arq)
            arq.close()               
        
        # Se o objeto pesquisado já estiver no cache, executar:
        elif bol == True:
            self.df = self.cache[self.text]
            
    def save_df(self):
        nome = input('Entre com o nome que deseja salvar o dataframe: ')
        self.df.to_csv((nome + '.csv'), encoding='utf-8', index=True)
            
    def save_cache(self):
        for i in self.cache:
            self.cache[i].to_csv(([i] + '_dataframe.csv'), encoding='utf-8', index=True)
            
                
    

# Funções auxiliares
def string_busca(lista, palavra):
    bol = False
    i = 0
    while bol == False and i < len(lista):
        if palavra in lista[i]:
            bol = True
        i += 1
    return bol

def printa(lista):
    for i in lista:
        print(f'- {i}')
    print("\n")
