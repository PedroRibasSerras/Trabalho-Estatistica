import pandas as pd
import matplotlib
matplotlib.use('TkAgg') # case does not matter tkaGg, TkAgg will do
import matplotlib.pyplot as plt
import numpy as np
import tkinter

import geoviews as gv
import geoviews.feature as gf
from geoviews import dim
from geoviews import opts
gv.extension('bokeh', 'matplotlib')

import holoviews as hv
import hvplot.pandas

import panel as pn
pn.extension()

from vega_datasets import data as vds

import cartopy
import cartopy.feature as cf
from cartopy import crs as ccrs

import geocoder

import json
import re
import json
import glob
import datetime

# Gerando os URL dos .csv
caminho = r'dados/dados-sp-'
todos_dados_csv = glob.glob(caminho + "*.csv")

# Colunas que incluem datas
datas = ['dataNotificacao', 'dataInicioSintomas', 'dataTeste', 'dataEncerramento']

# Colunas a serem lidas
cols = ["dataNotificacao", "dataInicioSintomas", "sintomas", "profissionalSaude", "cbo","condicoes",
        "dataTeste", "tipoTeste", "resultadoTeste", "sexo", "municipio", "municipioIBGE", "estadoNotificacao",
        "estadoNotificacaoIBGE", "idade", "dataEncerramento", "evolucaoCaso", "classificacaoFinal"]

# Carregando os dados
dados = pd.concat((pd.read_csv(f, sep=';', encoding='latin1', parse_dates=datas, usecols=cols, infer_datetime_format = False) for f in todos_dados_csv), ignore_index = True)

# Exclui as linhas cujas colunas indicadas abaixo sao null
dados.dropna(subset = ["dataNotificacao", "sexo", "municipio", "municipioIBGE", "estadoNotificacao", "estadoNotificacaoIBGE"], inplace = True)

# Exclui os dados Cancelados
dados.drop(dados[dados['evolucaoCaso'] == 'Cancelado'].index, inplace = True)

# Exclui os dados que possuem datas fora do escopo esperado
data_limite_inferior = np.datetime64('2020-01-01', 'ns') # Comeco da pandemia
data_limite_superior = np.datetime64('2021-03-25', 'ns') # A publicacao dos dados mais recentes ocorreram nesse dia
for data in datas:
    dados[data] = pd.to_datetime(dados[data], utc=True).dt.tz_localize(None) # Retira o fuso horario
    dados.drop(dados[(dados[data] < data_limite_inferior) | (dados[data] > data_limite_superior)].index, inplace = True) # Exclui

dados[dados['idade'] > 116] = float("NaN") # Exclui idades invalidas
dados.reset_index(drop=True, inplace = True) # Realoca os indices depois das exclusoes

sintomas = dados["sintomas"]
classificacaoFinal = dados["classificacaoFinal"]

MatrizTeste = []
teste4 = 'Nan'

for i in range(len(sintomas)):
    teste = []
    teste2 = []
    teste3 = []
    if(type(sintomas[i]) == str):
        teste.append(sintomas[i].split(', '))

        for palavra in teste[0]:
            teste2.append(palavra.split(','))
        for lista in teste2:
            teste3.append(lista[0])
        teste[0] = teste3
        
    else:
        teste.append(teste4) 
    
    teste.append(classificacaoFinal[i])
    MatrizTeste.append(teste)

pandaSintomas = pd.DataFrame(MatrizTeste)

contador_palavras = {}
for linhas in pandaSintomas[0]:
    for palavra in linhas:
        contador_palavras.setdefault(palavra, 0)
        contador_palavras[palavra] += 1

plt.bar(contador_palavras.keys(), contador_palavras.values(), color='red')

#plt.xticks(contador_palavras.keys())
#plt.yticks(contador_palavras.values())

plt.ylabel("quantidade de pessoas")
plt.xlabel('sintomas')
plt.title('pessoas x sintomas')

plt.show()