#importando as bibliotecas
import pandas as pd
import json
import numpy as np
import traceback

#extraindo os dados na forma json
with open('seriesInfo','r') as a:
    data = json.load(a)

#transformando os dados de json para dataframe
df = pd.DataFrame (data)
#configurando para mostrar todas as linha do dataframe
pd.set_option('display.max_rows', df.shape[0]+1)

#conferindo o numero de nulos no dataset#
print(df.isnull().sum())

#df1=df
df1 = df.copy()

df1.columns

#como os dados foram extraidos em formato de string,as chaves vieram juntas com as strings.Vamos retirar essas chaves
df1['nome'] = df1['nome'].apply(lambda a: str(a).replace('[',''))
df1['nome'] = df1['nome'].apply(lambda a: str(a).replace(']',''))
df1['nome'] = df1['nome'].apply(lambda a: str(a).replace("'",''))
df1['nome'] = df1['nome'].apply(lambda a: str(a).replace('"',''))
df1['infoGeral'] = df1['infoGeral'].apply(lambda a: str(a).replace('[',''))
df1['infoGeral'] = df1['infoGeral'].apply(lambda a: str(a).replace(']',''))
df1['infoGeral'] = df1['infoGeral'].apply(lambda a: str(a).replace("'",''))
df1['notas'] = df1['notas'].apply(lambda a: str(a).replace('[',''))
df1['notas'] = df1['notas'].apply(lambda a: str(a).replace(']',''))
df1['notas'] = df1['notas'].apply(lambda a: str(a).replace("'",''))
df1['nomeAtores'] = df1['nomeAtores'].apply(lambda a: str(a).replace('[',''))
df1['nomeAtores'] = df1['nomeAtores'].apply(lambda a: str(a).replace(']',''))
df1['nomeAtores'] = df1['nomeAtores'].apply(lambda a: str(a).replace("'",''))
df1['aonde_assistir'] = df1['aonde_assistir'].apply(lambda a: str(a).replace('[',''))
df1['aonde_assistir'] = df1['aonde_assistir'].apply(lambda a: str(a).replace(']',''))
df1['aonde_assistir'] = df1['aonde_assistir'].apply(lambda a: str(a).replace("'",''))
df1['sinopse'] = df1['sinopse'].apply(lambda a: str(a).replace('[',''))
df1['sinopse'] = df1['sinopse'].apply(lambda a: str(a).replace(']',''))
df1['sinopse'] = df1['sinopse'].apply(lambda a: str(a).replace("'",''))

#os valores vazio do dataset estão no formato de aspas simples,vamos substituir essas aspsas pelo numpy.nan,com o intuito de facilitar o tartamento dos dados depois
df1.replace('', np.nan, inplace=True)

#criando um dataframe com dois valores(True ou False) se o for nulo o valor é = a True
null_values = df1.isnull()
#percorrendo todas linhas e colunas do dataframe
for i, row in null_values.iterrows():
    #se o valor daquela linha e coluna for igual a True então a condição é aceita
    if row.any():
        #fazendo uma interação usando o iteritems,col e val,coluna vai armazenar cada coluna daquela linha e o val o valor,se o valor for nulo ou True,vamos pegar o nome da coluna e adcionar no colunas nulas
        colunas_nulas = [col for col, val in row.iteritems() if val]
        print(f'Linha {i} tem valores nulos na(s) coluna(s): {colunas_nulas}')


#separando a coluna "notas" em duas listas,nota_da_critica e a nota_do_publico
notas=[]
nota_da_critica =[]
nota_do_publico =[]

#iterando sobre cada item da coluna notas
for i in df1['notas']:
    #dividindo as notas pela virgula 
    i=i.split(",")
    #adicionando as duas notas mas separada por vigula
    notas.append(i)
    #iterando agora sobre a lista "notas"
for x in range(len(notas)):
    #se o tamanho da lista dentro da lista notas for igual 2,então a condiçao e aceita
    if len(notas[x]) == 2:
        #nota da critica é a primeira nota
        nota_da_critica.append(notas[x][0])
        #nota do público  é a segunda nota
        nota_do_publico.append(notas[x][1])
    else:
        #após uma verificação foi notado que todas as notas faltantes são da crítica
        nota_da_critica.append(np.nan)
        nota_do_publico.append(notas[x][0])

df2 = df1.copy()
#como vamos adidcionar as colunas da nota da critica e nota do publico,vamos excuir a coluna nota
df2.drop(['notas'],axis=1,inplace=True)

#adicionando as notas ao df,removendo o simbolo da porcentagem e transformando em valores númericos,ignorando os valores nulos
df2['notas_da_critica'] =pd.Series(nota_da_critica)
df2['notas_do_publico'] =pd.Series(nota_do_publico)
df2['notas_da_critica'] = df2['notas_da_critica'].apply(lambda a: str(a).replace('%',''))
df2['notas_do_publico'] = df2['notas_do_publico'].apply(lambda a: str(a).replace('%',''))
df2['notas_do_publico'].astype(int,errors='ignore')
df2['notas_da_critica'].astype(int,errors='ignore')
df2.dtypes
#separando a coluna infoGeral em 3 novas colunas["Tv_network","Genero","Data de lançamento"]
Tv_network=[]
genre=[]
premiere_date=[]
year=[]
#iterando sobre cada item da coluna infoGeral
for i in df2['infoGeral']:
#separando valores por virgula
    i=i.split(",")
    #tv_netowrk pegando o primero valor após a separação
    Tv_network.append(i[0].split(":")[1])
     #premiere_Date pegando o segundo valor após a separação
    premiere_date.append(i[1].split(":")[1])
     #year pegando o terceiro valor após a separação
    year.append(i[2])
     #genre pegando o quarto valor após a separação
    genre.append(i[3].split(":")[1])


df3=df2.copy()
#adicionando as novas colunas ao df e concatenando as colunas ano com o mes_dia 
df3['Ano'] =pd.Series(year)
df3['mes_dia'] =pd.Series(premiere_date) 
df3['Genero'] =pd.Series( genre)
df3['Tv_network'] =pd.Series(Tv_network)
df3['Data_de_lancamento'] = pd.to_datetime(df3["Ano"] + "/" + df3["mes_dia"])
df3['Data_de_lancamento'] = pd.to_datetime(df3['Data_de_lancamento'], format='%Y-%m-%d')

#excluindo as colunas que não serão mais úteis
df3.drop(['infoGeral'],axis=1,inplace=True)
df3.drop(['Ano'],axis=1,inplace=True)
df3.drop(['mes_dia'],axis=1,inplace=True)

#separando a coluna nomeAtores em duas novas colunas produtores e atores
criadores_e_atores = []
col_name = 'nomeAtores'

#itertando no df3
for i, row in df3.iterrows():
    #para evitar erros durante loop ja vamos adicionar os valores nulos na lista
    if pd.isnull(row[col_name]):
        criadores_e_atores.append(np.nan)
        #caso o valor nao seja nulo o loop começa
    else:
        #transformando o valor em str
        result = str(row[col_name])
        #procurando o ,'Starring:' na str
        pos = result.find('Starring:')
        #caso seja a primeria ou a segunda palavra a condição e aceita
        if pos != 0 and pos != 1:
            result = result[:pos] + ',Starring:' + result[pos+9:]
            criadores_e_atores.append(result)
        #caso esteja em outro lugar a condição de biaxo e aceita
        elif pos == 0 or pos == 1:
            result = str(row[col_name])
            criadores_e_atores.append(result)

#se o valor da lista nao for nulo entao vai substituir a aspas duplas pelo vazio
for i, item in enumerate(criadores_e_atores):
    if not pd.isnull(item):
        criadores_e_atores[i] = item.replace('"', '')

#separando a lista criadores_e_atores em duas listas creators e starring
creators=[]
starring=[]
linha = 0

try:
    #se o valor na lista for nulo entao adiciona nulo para as duas listas
    for x in criadores_e_atores:
        if pd.isnull(x):
            creators.append(np.nan)
            starring.append(np.nan)
        else:
            #caso ao contrario o loop começa
            linha += 1
            t=x.split(',Starring:')
            #vamos dividir a string em duas partes se o tamanho da divisão vor igual 2 o creators adiciona o primeiro elemento e os atores o segundo
            if len(t) == 2:
                creators.append(t[0].split(':')[1])
                starring.append(t[1])
            #se o valor dda divisao for igual adiciona nulos para os creators e valor para os atores
            elif len(t) == 1:
                creators.append(np.nan)
                starring.append(t[0].split(':')[1])
except Exception as e:
    print(f"Ocorreu um erro na linha {linha}:", e)
    print("Em:", traceback.format_exc())

df4=df3.copy()
#ecluindo uma coluna pois vamos separa-la em duas novas
df4.drop('nomeAtores',axis=1,inplace=True)
df4['Produtores'] =pd.Series(creators)
df4['Atores'] =pd.Series(starring)


df5=df4.copy()

#transformando a coluna atores em colunas novas a paritr da virgula e renomeando elas
atores_df = df5['Atores'].str.split(',', expand=True)
df5 = pd.concat([df5, atores_df.rename(columns={0: 'ator_1', 1: 'ator_2', 2: 'ator_3', 3: 'ator_4', 4: 'ator_5'})], axis=1)

df5.drop('Atores',axis=1,inplace=True)
df5.head()


df6=df5.copy()

#transformando a coluna aonde_assistir em colunas novas a paritr da virgula e renomeando elas

assistir_df = df6['aonde_assistir'].str.split(',', expand=True)
df6 = pd.concat([df6, assistir_df.rename(columns={0: 'opçao_1', 1: 'opçao_2', 2: 'opçao_3', 3: 'opçao_4', 4: 'opçao_5'})], axis=1)

df6.drop('aonde_assistir',axis=1,inplace=True)
df6.dtypes

df6.head()
