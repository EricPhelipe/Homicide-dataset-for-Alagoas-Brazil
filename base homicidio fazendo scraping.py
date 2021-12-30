# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 12:12:47 2021

@author: ericp
"""
import pandas as pd
import requests
import os
from bs4 import BeautifulSoup 
import tabula
import unicodedata
import matplotlib.pyplot as plt
import seaborn as sns

# Web scraping de dados referentes a homicídios em Alagoas.
urls = [ 'http://seguranca.al.gov.br/estatisticas/16/', 'http://seguranca.al.gov.br/estatisticas/27/', 
        'http://seguranca.al.gov.br/estatisticas/32/', 'http://seguranca.al.gov.br/estatisticas/39/', 
        'http://seguranca.al.gov.br/estatisticas/60/', 'http://seguranca.al.gov.br/estatisticas/66/' ]

list1 = []

for url in urls:
    requests.get(url)
    soup = BeautifulSoup(requests.get(url).text, 'html.parser' )
    for i in soup.find_all('a', href=True):
        x = i['href']
        if(x[-4:]=='.pdf'):
            list1.append(i['href'])


z=0
ax = []
for j in list1:
    if z == 0:
        ax = tabula.read_pdf(list1[0], pages='all')
        z += 1      
    else:
        ax = ax + tabula.read_pdf(list1[0+z], pages='all')
        z += 1

# Junção dos data frames de todos os anos.
b = pd.concat(ax[0:], axis=0).reset_index()
b.drop(['index'], axis=1, inplace=True)

# Mudando nomes das colunas para manipulação da base.
b.columns = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','50']

# Função que permite a junção das diferentes colunas com datas, horas,  nomes, cidades e bairros.
def ar(arg):
    if arg == arg:
        return arg
    else:
        return ' '

# Junção de colunas com nomes, cidades e bairros.
aq = ['1','2','7', '8', '9','10', '15', '16', "17"]
for j in aq:
    b[j] = b[j].map(ar)  
b['18'] = b['1'] + ' - ' + b['2'] + ' ' + b['9'] + ' ' + b['10']
b['23'] = b['7'] + ' ' + b['15']
b['24'] = b['8'] + ' ' + b['16'] + ' ' + b['17']
b['25'] = b['23'] + ' - ' + b['24']
b.drop(['1', '2', '7', '8', '9', '10','13', '14', '15', '16', '17', '23', '24' ], axis=1, inplace=True )
b['51'], b['52'] = b['12'].str.split(' ', 1).str

# Função para ajuste de colunas com idades.
def al(arg2):
    if arg2 == arg2:
        return arg2
    else:
        return 0
    
# Ajuste de coluna idade.
ap = ['3', '11', '51']
for r in ap:
    b[r] = b[r].map(al)

#b['3'].astype(int)
b['3'].loc[b['3'] == '33.0 ..']
b['3'][5964] = 33
b['3'] = b['3'].astype(int)
b['11'] = b['11'].astype(int)
#b['51'].astype(int)
b['51'].loc[b['51'] == 'Resistência']
b[b['51'] == 'Resistência'] = 0
b['51'].loc[b['51'] == 'Homicídio']
b[b['51'] == 'Homicídio'] = 0
b['51'] = b['51'].astype(int)
b['20'] = b['3'] + b['11'] + b['51']
b['5'] = b['5'].map(ar)
b['52'] = b['52'].map(ar)
b['53'] = b['5'] + b['52']
b.drop(['3', '5', '11', '12', '51', '52'], axis=1, inplace=True )

# Dropando linhas com observações mal registradas.
b.drop(b[b['53'] == '  '].index, inplace=True)
b.drop(b[b['53'] == 0].index, inplace=True)

# Funções para ajustes de nomes, datas e horas.
def wa(arg4):
    if ' - ' in arg4:
        return arg4.replace(' - ', ' ')
    else:
        pass
def wo(arg5):
    if '  ' in arg5:
        return arg5.replace('  ', '')
    else:
        pass

def jy(arg6):
    if '1' in arg6:
        return arg6
    elif '0' in arg6:
        return arg6
    elif '2' in arg6:
        return arg6
    else:
        return ' '
 
def ref(arg8):
    if '/' in arg8:
        return ' '
    else:
            return arg8
        
def wol(arg15):
    if ' ' in arg15:
        return arg15.replace(' ', '')
    else:
        pass       
 # Ajustes de datas, horas e nomes .
b['25'] = b['25'].map(wo)
b['18'] = b['18'].map(wa)
b['18'] = b['18'].map(wo)
b['34'], b['35'] = b['18'].str.split(' ', 1).str
b['36'], b['37'] = b['35'].str.split(' ', 1).str
b['36'] = b['36'].map(ar)
  
b['40'] = b["36"].map(jy)
b['54'], b['55'] = b['40'].str.split('A', 1).str
b['56'], b['57'] = b['55'].str.split('A', 1).str


b['41'] = b['34'].map(ref)

b['58'], b['59'] = b['41'].str.split('A', 1).str
b['60'], b['61'] = b['59'].str.split('A', 1).str
b['57'] = b['57'].map(ar)
b['61'] = b['61'].map(ar)
b['54'] = b['54'].replace('00', '0').replace('01', '1').replace('02', '2').replace('03', '3').replace('04', '4').replace('05', '5').replace('06', '6').replace('07', '7').replace('08', '8').replace('09', '9')
b['57'] = b['57'].replace('00', '0').replace('01', '1').replace('02', '2').replace('03', '3').replace('04', '4').replace('05', '5').replace('06', '6').replace('07', '7').replace('08', '8').replace('09', '9')
b['58'] = b['58'].replace('00', '0').replace('01', '1').replace('02', '2').replace('03', '3').replace('04', '4').replace('05', '5').replace('06', '6').replace('07', '7').replace('08', '8').replace('09', '9')
b['61'] = b['61'].replace('00', '0').replace('01', '1').replace('02', '2').replace('03', '3').replace('04', '4').replace('05', '5').replace('06', '6').replace('07', '7').replace('08', '8').replace('09', '9')
b['62'] = b['54'] + b['57'] + b['58'] + b['61']


b['62'] = b['62'].map(wol)
#b['62'].astype(int)     
b['62'].loc[b['62'] == ''].count()   
b.drop(b[b['62'] == ''].index, inplace=True)
#b['42'].astype(int) 
b.drop(b[b['62'] == 'Olho'].index, inplace=True)
#b['42'].astype(int) 
b.drop(b[b['62'] == 'CHOQUE18'].index, inplace=True)
#b['42'].astype(int) 
b.drop(b[b['62'] == 'Fátima'].index, inplace=True)
#b['42'].astype(int) 
b.drop(b[b['62'] == 'Manoel'].index, inplace=True)
#b['42'].astype(int) 
b.drop(b[b['62'] == 'José'].index, inplace=True)
b['62'] = b['62'].astype(int) 

def ref(arg9):
    if '0' in arg9:
        return ''
    elif '1' in arg9:
        return ''
    elif '2' in arg9:
        return ''
    else:
            return arg9
b['43'] = b['36'].map(ref)
b['44'] = b['43'] + ' ' + b['37']

b.drop(['18', '35', '36', '37', '40', '41', '43', '54', '55', '56', '57', '58', '59', '60', '61'], axis =1, inplace=True)

def refi(arg10):
    if '/' in arg10:
        return arg10
    else:
            return ''
b['34'] = b['34'].map(refi)

def ar1(arg11):
    if arg11 == arg11:
        return arg11
    else:
        return ' - '

ty = ['4', '6', '50', '44' ]

for r in ty:
    b[r] = b[r].map(ar1)
    
    
b.columns = ['SEXO', 'TIPO_DE_MORTE', 'COR', 'LOCAL', 'IDADE', 'SUBJETIVIDADE_COMPLEMENTAR', 'DATA', 'HORA', 'NOME']
    
# Ajustando as datas faltantes.
def ds(arg12):
    for i in arg12:
        if '/' in arg12:
            return arg12
        else:
            return i[-i]
b['DATA'] = b['DATA'].map(ds)
b['DATA'] = b['DATA'].fillna(axis=0, method='ffill')
b['DATA'] = pd.to_datetime(b['DATA'], dayfirst=True, format='%d/%m/%Y')

b = b.sort_values(['DATA', 'HORA'], ascending=True)

# Criando colunas de dias, meses e anos.
b['DIA'] = pd.DatetimeIndex(b['DATA']).day
b['MES'] = pd.DatetimeIndex(b['DATA']).month
b['ANO'] = pd.DatetimeIndex(b['DATA']).year


# Ajuste para serapar o primeiro nome.

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
b['NOME'] = b['NOME'].map(strip_accents)
def asd(arg14):
    if arg14 in arg14:
        return arg14.upper()
    else:
        pass

b['NOME'] = b['NOME'].map(asd)

b['PRIMEIRO NOME'], b['Y'] = b['NOME'].str.split(' ', 1).str


def wsx(arg15):   
    if "A" in arg15:
        return arg15
    elif "E" in arg15:
        return arg15
    elif "I" in arg15:
        return arg15
    elif "O" in arg15:
        return arg15
    elif "U" in arg15:
        return arg15
    elif "Y" in arg15:
        return arg15
    else:
        return '-'
    
def ws(arg16):   
    if "A" in arg16:
        return '-'
    elif "E" in arg16:
        return '-'
    elif "I" in arg16:
        return '-'
    elif "O" in arg16:
        return '-'
    elif "U" in arg16:
        return '-'
    elif "Y" in arg16:
        return '-'
    else:
        return arg16
b['PRIMEIRO NOME12'] = b['PRIMEIRO NOME'].map(wsx)
b['PRIMEIRO NOMEx'] = b['PRIMEIRO NOME'].map(ws)
b['P'] = b['PRIMEIRO NOMEx'] + b['Y']
b['PRIMEIRO NOME1'], b['U'] = b['P'].str.split(' ', 1).str
b['PRIMEIRO NOME'] = b['PRIMEIRO NOME'] + b['PRIMEIRO NOME1']
b['PRIMEIRO NOME'], b['T'] = b['PRIMEIRO NOME'].str.split('-', 1).str

b.drop(['Y', 'PRIMEIRO NOME12', 'PRIMEIRO NOME1', 'P','PRIMEIRO NOMEx', 'U', 'T'], axis=1, inplace=True)

b['PRIMEIRO NOME'] = b['PRIMEIRO NOME'].map(wsx)
os.chdir('C:/Users/ericp/Documents/PIMES/Python/Nova pasta')
b['OCORRÊNCIAS'] = 1


# Retirando dias da semana
Dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
def aio(arg50):
    if arg50 == arg50:
        return Dias[arg50.weekday()]
    else:
        pass
b['DIA DA SEMANA'] = b['DATA'].map(aio)

#Padronizando tipos de morte
b['TIPO_DE_MORTE'] = b['TIPO_DE_MORTE'].map(asd)
def xds(arg51):
    if 'BRANCA' in arg51:
        return 'ARMA BRANCA'
    elif 'ESPAN' in arg51:
        return 'ESPANCAMENTO'
    elif 'LINCHA' in arg51:
        return 'ESPANCAMENTO'
    elif 'ATROPELA' in arg51:
        return 'ATROPELAMENTO'
    elif 'OUTROS' in arg51:
        return 'OUTROS'
    elif 'NI' in arg51:
        return 'OUTROS'
    elif ' - ' in arg51:
        return 'OUTROS'
    elif 'ACIDENTE' in arg51:
        return 'OUTROS'
    elif 'QUEDA' in arg51:
        return 'OUTROS'
    elif 'QUEIMADURA' in arg51:
        return 'CARBONIZADO'
    elif '/' in arg51:
        return 'PAF/BRANCA'
    elif 'FB' in arg51:
        return 'PAF/BRANCA'
    else:
        return arg51
b['TIPO_DE_MORTE'] = b['TIPO_DE_MORTE'].map(xds)
b['TIPO_DE_MORTE'].value_counts()
#b.drop(b[b['PRIMEIRO NOME'] == 'NAO'].index, axis=0, inplace=True) 
#b.to_excel('BASEHOMICIDIOSCOMNOMES.xlsx')



# Gráfico contagem anual de homicídios.
baseano = b.groupby(['ANO']).agg({'OCORRÊNCIAS':'count'}).reset_index()
plt.figure(figsize=(15, 10))
sns.pointplot(baseano["ANO"],baseano['OCORRÊNCIAS'],color='black', linestyles='--')
plt.ylabel("")
plt.yticks( fontsize=25)
plt.locator_params(axis='x', nbins=12)
plt.xticks( rotation = 55, fontsize=20)
plt.xlabel('')
plt.title("Contagem anual de ocorrências",loc='left',fontsize=30)


# base para gráficos da média por mês.
basemes = b.groupby(['MES']).agg({'OCORRÊNCIAS':'count'}).reset_index()
xs = ['1','2','3','4','5','6','7','8','9','10','11','12']
nms = ['JAN', 'FEV','MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']
nomes_meses = pd.Series(xs, index=nms).reset_index()
nomes_meses.columns = ['MES1', 'MES2']
nomes_meses['MES2'] = nomes_meses['MES2'].astype(int)
basemes = pd.concat([basemes, nomes_meses], axis=1)
basemes.drop(['MES', 'MES2'], axis=1, inplace=True)

def axz(arg30):
    if arg30 == 704:
        return 704/5
    else:
        return int(arg30)/6
    
basemes['OCORRÊNCIAS'] = basemes['OCORRÊNCIAS'].map(axz)   

# Gráfico médias mensais de homicídios.
plt.figure(figsize=(15, 10))
sns.pointplot(basemes["MES1"],basemes['OCORRÊNCIAS'],color='gray', linestyles='--')
plt.ylabel("")
plt.yticks( fontsize=25)
plt.locator_params(axis='x', nbins=12)
plt.xticks( rotation = 55, fontsize=20)
plt.xlabel('')
plt.title("Médias mensais de ocorrências",loc='left',fontsize=30)

# base para gráficos da média por dia da semana
basedia = b.groupby(['DATA', 'DIA DA SEMANA']).agg({'OCORRÊNCIAS':'sum'}).reset_index()
basedia['OCORRÊNCIA DE DIAS'] = 1
basedia = basedia.groupby(['DIA DA SEMANA']).agg({'OCORRÊNCIAS': 'sum', 'OCORRÊNCIA DE DIAS':'sum'}).reset_index()
basedia['MÉDIA'] =  basedia['OCORRÊNCIAS'] / basedia['OCORRÊNCIA DE DIAS']
basedia['DIA'] = ['6', '2', '3', '0', '4', '5', '1']
basedia['DIA'] = basedia['DIA'].astype(int)
basedia = basedia.sort_values(by=['DIA'], ascending = True)

# Gráficos médias por dia da semana
plt.figure(figsize=(15, 10))
sns.pointplot(basedia['DIA DA SEMANA'], basedia['MÉDIA'],color='red', linestyles='--')
plt.ylabel("")
plt.yticks( fontsize=25)
plt.locator_params(axis='x', nbins=12)
plt.xticks( rotation = 55, fontsize=20)
plt.xlabel('')
plt.title("Médias diárias de ocorrências",loc='left',fontsize=30)

# base para gráficos da média horária.
basehora = b.groupby(['DATA', 'HORA']).agg({'OCORRÊNCIAS':'sum'}).reset_index()
basehora['OCORRÊNCIA DE HORAS'] = 1
basehora = basehora.groupby(['HORA']).agg({'OCORRÊNCIAS': 'sum', 'OCORRÊNCIA DE HORAS':'sum'}).reset_index()
basehora['MÉDIA'] =  basehora['OCORRÊNCIAS'] / basehora['OCORRÊNCIA DE HORAS']

# Gráficos média horária.
plt.figure(figsize=(15, 10))
sns.pointplot(basehora['HORA'],basehora['MÉDIA'],color='blue', linestyles='--')
plt.ylabel("")
plt.yticks( fontsize=25)
plt.locator_params(axis='x', nbins=12)
plt.xticks( rotation = 55, fontsize=20)
plt.xlabel('')
plt.title("Médias horárias de ocorrências",loc='left',fontsize=30)



# Gráficos de ocorrências por idade 

baseidade = b.groupby(['IDADE']).agg({'OCORRÊNCIAS':'sum'}).reset_index()
baseidade.drop(baseidade[baseidade['IDADE'] == 0].index, axis=0, inplace=True)

plt.figure(figsize=(15, 10))
sns.barplot(x = baseidade['IDADE'], y = baseidade['OCORRÊNCIAS'] )

plt.ylabel("")
plt.yticks( fontsize=20)
plt.locator_params(axis='x', nbins=20)
plt.xticks( rotation = 55, fontsize=15)
plt.xlabel('')
plt.title("Ocorrências por idade",loc='left',fontsize=30)


# padronização para gráfico de proporção por tipo de morte
basetm = b.copy()
basetm['TIPO_DE_MORTE'].value_counts()

def trwq(arg52):
    if 'CARBONIZADO' in arg52:
        return 'OUTROS'
    elif 'ATROPELAMENTO' in arg52:
        return 'OUTROS'
    elif 'AFOGAMENTO' in arg52:
        return 'OUTROS'
    elif 'INTOXICAÇÃO' in arg52:
        return 'OUTROS'
    elif 'OVERDOSE' in arg52:
        return 'OUTROS'
    else:
        return arg52
basetm['TIPO_DE_MORTE'] = basetm['TIPO_DE_MORTE'].map(trwq)

# Gráfico de proporção por tipo de morte
plt.figure(figsize=(7, 7))
basetm['TIPO_DE_MORTE'].value_counts().plot.pie(autopct = "%1.0f%%", 
                                          colors =sns.color_palette("rainbow",6), wedgeprops = {"linewidth":2,"edgecolor":"white"})
my_circ = plt.Circle((0,0),.7,color = "white") # Experimenta tirar essa linha do plot
plt.gca().add_artist(my_circ)
plt.ylabel("")
plt.title("Proporção do tipo de morte",fontsize=15)



# Gráfico de proporção de mortes por sexo 
plt.figure(figsize=(7, 7))
baseidade = b
baseidade.drop(baseidade[baseidade['SEXO'] == ' - ' ].index, axis=0, inplace=True)
baseidade['SEXO'].value_counts().plot.pie(autopct = "%1.0f%%", 
                                          colors =sns.color_palette("rainbow",6), wedgeprops = {"linewidth":2,"edgecolor":"white"})
plt.ylabel("")
plt.title("Proporção de mortes por sexo",fontsize=15)


# Gráfico de proporção da subjetividade complementar
plt.figure(figsize=(7, 7))
b['SUBJETIVIDADE_COMPLEMENTAR'].value_counts().plot.pie(autopct = "%1.0f%%", 
                                          colors =sns.color_palette("rainbow",6), wedgeprops = {"linewidth":2,"edgecolor":"white"})
my_circ = plt.Circle((0,0),.7,color = "white") # Experimenta tirar essa linha do plot
plt.gca().add_artist(my_circ)
plt.ylabel("")
plt.title("Proporção da subjetividade complementar",fontsize=15)
b.columns

