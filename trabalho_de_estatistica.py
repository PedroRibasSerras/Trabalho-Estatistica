import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#import plotly.express as px
import re
#import plotly.graph_objs as go
import json

dados = pd.read_csv('dados-sp-1.csv', sep=";", encoding='latin1')

dados[dados['idade'] > 116] = float("NaN")
print(dados.describe())

dados.hist(column='idade', bins=116)
plt.show()
dados['sexo'].value_counts().plot(kind='bar')
plt.show()
print(dados.head())