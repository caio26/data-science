import pandas as pd
import plotly.express as px
import numpy as np
from unicodedata import normalize
from faker import Faker
import datetime

# Lendo o arquivo Connections.xlsx e criando um dataframe conexoes
conexoes = pd.read_excel('/content/Connections.xlsx')

# Mostra as primeiras linhas do dataframe
conexoes.head()

# Removendo a coluna 'Email Address' do dataframe conexoes
conexoes.drop(labels = ['Email Address'], axis=1, inplace=True)

# Mostra as primeiras linhas do dataframe conexoes após a remoção da coluna
conexoes.head()

# Verificando a quantidade de valores nulos em cada coluna do dataframe conexoes
conexoes.isna().sum()

# Verificando a quantidade de linhas e colunas do dataframe conexoes
conexoes.shape

# Removendo as linhas que possuem valores nulos no dataframe conexoes
conexoes.dropna(inplace=True)

# Verificando a quantidade de linhas e colunas do dataframe conexoes após a remoção de valores nulos
conexoes.shape

# Verificando novamente a quantidade de valores nulos em cada coluna do dataframe conexoes
conexoes.isna().sum()

# Criando uma nova coluna 'Full Name' no dataframe conexoes, que será a junção das colunas 'First Name' e 'Last Name'
conexoes['Full Name'] = conexoes['First Name'] + ' ' + conexoes['Last Name']

# Mostra as primeiras linhas do dataframe conexoes com a nova coluna 'Full Name'
conexoes.head()

# Função que remove acentos de um texto
def remove_acentos(texto):
  source = texto
  target = normalize('NFKD', source).encode('ASCII','ignore').decode('utf-8')
  return target

# Aplicando a função 'remove_acentos' na coluna 'Position' do dataframe conexoes
conexoes['Position'] = conexoes['Position'].apply(remove_acentos)

# Mostra as primeiras linhas do dataframe conexoes após a remoção de acentos na coluna 'Position'
conexoes.head()

# Verificando a quantidade de valores nulos em cada coluna do dataframe conexoes
conexoes.isna().sum()

# Verificando a quantidade de linhas e colunas do dataframe conexoes
conexoes.shape

# Removendo as linhas que possuem valores nulos no dataframe conexoes
conexoes.dropna(inplace=True)

# Verificando a quantidade de linhas e colunas do dataframe conexoes após a remoção de valores nulos
conexoes.shape

# Verificando novamente a quantidade de valores nulos em cada coluna do dataframe conexoes
conexoes.isna().sum()

# Criando uma nova coluna 'Full Name' no dataframe conexoes, que será a junção das colunas 'First Name' e 'Last Name'
conexoes['Full Name'] = conexoes['First Name'] + ' ' + conexoes['Last Name']

# Mostra as primeiras linhas do dataframe conexoes com a nova coluna 'Full Name'
conexoes.head()

# Lendo o arquivo Invitations.csv e criando um dataframe convites
convites = pd.read_csv('Invitations.csv')

# Mostrando as colunas do dataframe convites
convites.columns

# Verificando a quantidade de linhas e colunas do dataframe convites
convites.shape

# Mostra as primeiras 30 linhas do dataframe convites
convites.head(30)

# Verifica a quantidade de valores nulos em cada coluna do dataframe convites
convites.isna().sum()

# Mostra as primeiras 10 linhas do dataframe convites onde a coluna "Message" não é nula
convites[convites['Message'].notnull()].head(10)

# Mostra a quantidade de linhas e colunas do dataframe convites
convites.shape

# Seleciona apenas as linhas do dataframe convites em que a coluna "Direction" é igual a "INCOMING"
convites = convites[convites['Direction'] == 'INCOMING']
convites.shape

# Mostra os valores únicos da coluna "Direction" do dataframe convites
np.unique(convites['Direction'])

# Adiciona uma coluna vazia chamada "Company" ao dataframe convites
convites['Company'] = ''
convites.head()

# Mostra a quantidade de linhas do dataframe convites
len(convites)

# Redefine os índices do dataframe convites
convites = convites.reset_index(drop=True)
convites

# Itera sobre cada linha do dataframe convites e, para cada linha, atribui o valor da coluna "Company" do dataframe conexoes que corresponde ao nome da pessoa na coluna "From" do dataframe convites
for i in range(0, len(convites)):
  try:
    company = conexoes[conexoes['Full Name'] == convites['From'][i]]['Company'].values[0]
    convites['Company'][i] = company
  except:
    continue

# Remove as colunas "From", "To", "Sent At", "Message" e "Direction" do dataframe convites
convites.drop(labels=['From', 'To', 'Sent At', 'Message', 'Direction'], axis=1, inplace=True)
convites

# Salva o dataframe convites em um arquivo CSV
convites.to_csv('convites.csv')

# Remove as colunas "First Name", "Last Name" e "Full Name" do dataframe conexoes
conexoes.drop(labels=['First Name', 'Last Name', 'Full Name'], axis=1, inplace=True)
conexoes

# Importa a biblioteca Faker
from faker import Faker

# Cria uma instância do Faker
fake = Faker()

# Gera um nome falso aleatório
fake.name()

# Adiciona uma coluna vazia chamada "Full Name" ao dataframe conexoes
conexoes['Full Name'] = ''
conexoes.head()

# Redefine os índices do dataframe conexoes
conexoes = conexoes.reset_index(drop=True)

# Itera sobre cada linha do dataframe conexoes e, para cada linha, atribui um nome falso aleatório à coluna "Full Name"
for i in range(0, len(conexoes)):
  conexoes['Full Name'][i] = fake.name()

# Mostra as primeiras linhas do dataframe conexoes
conexoes.head()

# Salva o dataframe conexoes em um arquivo CSV
conexoes.to_csv('conexoes.csv')

# Lê o arquivo CSV "messages.csv" e salva os dados em um dataframe chamado "mensagens"
mensagens = pd.read_csv('messages.csv')

# Mostra as colunas do dataframe mensagens
mensagens.columns

# Verificando a forma do dataframe de mensagens
mensagens.shape

# Mostrando a primeira mensagem do dataframe
mensagens.head(1)

# Selecionando apenas a coluna CONTENT do dataframe
mensagens = mensagens['CONTENT']

# Mostrando as mensagens
mensagens

# Verificando se existem valores nulos na coluna de mensagens
mensagens.isna().sum()

# Removendo as mensagens nulas e verificando a nova forma do dataframe
mensagens.dropna(inplace=True)
mensagens.shape

# Salvando o dataframe de mensagens em um arquivo CSV
mensagens.to_csv('mensagens.csv')

# Importando as bibliotecas necessárias
import datetime
import pandas as pd
import plotly.express as px
import numpy as np

# Lendo o arquivo CSV de conexões e removendo a coluna Unnamed: 0
conexoes = pd.read_csv('conexoes.csv')
conexoes.drop(labels = ['Unnamed: 0'], axis = 1, inplace=True)

# Mostrando as primeiras linhas do dataframe de conexões
conexoes.head()

# Criando um gráfico de dispersão com a data de conexão e o nome completo do contato
grafico = px.scatter(conexoes, x = 'Full Name', y = 'Connected On')
grafico.show()

# Agrupando as conexões por data e contando o número de conexões por data
conexoes.groupby(by = 'Connected On').count()

# Criando um gráfico de linha com o número de novas conexões por data
grafico = px.line(conexoes.groupby(by = 'Connected On').count(), title = 'Novas conexões por data')
grafico.show()

# Definindo uma função para converter a data no formato YYYY-MM-DD para o mês correspondente
def converte_data_mes(data):
  return datetime.datetime.strptime(data, '%Y-%m-%d').strftime('%m')

# Aplicando a função de conversão de data para criar uma nova coluna com o mês de conexão
conexoes['Connected Month'] = conexoes['Connected On'].apply(converte_data_mes)
conexoes

# Agrupando as conexões por mês e contando o número de conexões por mês
conexoes.groupby(by = 'Connected Month').count()

# Criando um gráfico de linha com o número de novas conexões por mês
grafico = px.line(conexoes.groupby(by = 'Connected Month').count(), title = 'Novas conexões por mês')
grafico.show()

#Define a function to extract the year from a date string
def converte_data_ano(data):
  return datetime.datetime.strptime(data, '%Y-%m-%d').strftime('%Y')

#Aplica a função acima à coluna 'Connected On' do DataFrame 'conexoes',
#e cria uma nova coluna 'Connected Year' contendo apenas o ano
conexoes['Connected Year'] = conexoes['Connected On'].apply(converte_data_ano)

#Agrupa o DataFrame por ano e conta o número de entradas por ano
conexoes.groupby(by = 'Connected Year').count()

#Cria um gráfico de linha mostrando o número de conexões por ano usando Plotly
grafico = px.line(conexoes.groupby(by = 'Connected Year').count(), title = 'Novas conexões por ano')
grafico.show()

#Conta o número de ocorrências de cada empresa na coluna 'Company'
np.unique(conexoes['Company'], return_counts=True)

#Obtém a forma do DataFrame 'conexoes' (número de linhas, número de colunas)
conexoes.shape

#Conta o número de empresas únicas na coluna 'Company'
len(np.unique(conexoes['Company']))

#Cria um histograma da coluna 'Company' usando Plotly
grafico = px.histogram(conexoes['Company'])
grafico.show()

#Cria um treemap das colunas 'Company', 'Position' e 'Full Name' usando Plotly
grafico = px.treemap(conexoes, path=['Company', 'Position', 'Full Name'])
grafico.show()

#Conta o número de ocorrências de cada cargo na coluna 'Position'
np.unique(conexoes['Position'], return_counts=True)

#Obtém a forma do DataFrame 'conexoes' (número de linhas, número de colunas)
conexoes.shape

#Conta o número de cargos únicos na coluna 'Position'
len(np.unique(conexoes['Position']))

#Cria um histograma da coluna 'Position' usando Plotly
grafico = px.histogram(conexoes['Position'])
grafico.show()

#Conta o número de entradas na coluna 'Position' onde o valor é 'Cientista de Dados'
len(conexoes[conexoes['Position'] == 'Cientista de Dados'])

#Define uma função para padronizar os nomes dos cargos
def altera_cargo(cargo):
  novo_cargo = cargo
  if cargo == 'Data Scientist':
    novo_cargo = 'Cientista de Dados'
  elif cargo == 'Cientista de dados':
    novo_cargo = 'Cientista de Dados'
  return novo_cargo

#Aplica a função acima à coluna 'Position' do DataFrame 'conexoes'
conexoes['Position'] = conexoes['Position'].apply(altera_cargo)

#Conta o número de entradas na coluna 'Position' onde o valor é 'Cientista de Dados'
len(conexoes[conexoes['Position'] == 'Cientista de Dados'])

#Define um treemap do Pandas DataFrame 'conexoes' com hierarquia de caminho ('path') 'Position', 'Company' e 'Full Name'
grafico = px.treemap(conexoes, path = ['Position', 'Company', 'Full Name'])

#Mostra o gráfico treemap com o Plotly
grafico.show()

#Importa a biblioteca nltk
import nltk

#Importa a função edit_distance da biblioteca nltk.metrics.distance
from nltk.metrics.distance import edit_distance

#Calcula a distância de edição entre 'rain' e 'shine'
edit_distance('rain', 'shine')

#Calcula a distância de edição entre 'Analista de Dados' e 'Analista de dados'
edit_distance('Analista de Dados', 'Analista de dados')

#Separa os elementos do cargo 'analista de business intelligence' em uma lista
'analista de business intelligence'.split()

#Cria uma lista de bigramas (pares de palavras) para o cargo 'analista de business intelligence'
bigramas_cargo1 = list(nltk.bigrams('analista de business intelligence'.split(), pad_right=True, pad_left=True))
bigramas_cargo1

#Cria uma lista de bigramas (pares de palavras) para o cargo 'cientista de dados'
bigramas_cargo2 = list(nltk.bigrams('cientista de dados'.split(), pad_right=True, pad_left=True))
bigramas_cargo2

#Cria uma lista de bigramas (pares de palavras) para o cargo 'analista de dados'
bigramas_cargo3 = list(nltk.bigrams('analista de dados'.split(), pad_right=True, pad_left=True))
bigramas_cargo3

#Calcula a interseção entre dois conjuntos (set) de elementos
set(['A', 'B', 'C']).intersection(set(['C', 'D', 'E']))

#Calcula o tamanho da interseção entre as listas de bigramas dos cargos 1 e 2
len(set(bigramas_cargo1).intersection(set(bigramas_cargo2)))

#Calcula o tamanho da interseção entre as listas de bigramas dos cargos 1 e 3
len(set(bigramas_cargo1).intersection(set(bigramas_cargo3)))

#### Distância de Jaccard

# Número de itens em comum dividido pelo número total de itens distintos em dois conjuntos
# Usa n-gramas

#Definindo três cargos em formato de lista
cargo1 = 'analista de business intelligence'.split()
cargo2 = 'cientista de dados'.split()
cargo3 = 'analista de dados'.split()

#Exibindo as listas de cargos
cargo1, cargo2, cargo3

#Encontrando a interseção entre as palavras dos cargos 1 e 3
intersecao = set(cargo1).intersection(set(cargo3))
intersecao

#Encontrando a união entre as palavras dos cargos 1 e 3
uniao = set(cargo1).union(set(cargo3))
uniao

#Encontrando o tamanho da interseção e da união
len(intersecao), len(uniao)

#Calculando a distância de Jaccard entre os cargos 1 e 3
(len(uniao) - len(intersecao)) / len(uniao)

#Importando a função de distância de Jaccard
from nltk.metrics.distance import jaccard_distance

# Cargo 1 x Cargo 3
jaccard_distance(set(cargo1), set(cargo3))

# Cargo 1 x Cargo 2
jaccard_distance(set(cargo1), set(cargo2))

# Cargo 2 x Cargo 3
jaccard_distance(set(cargo2), set(cargo3))

#### Agrupamento dos cargos

# Exemplos baseados em: https://github.com/mikhailklassen/Mining-the-Social-Web-3rd-Edition/blob/master/notebooks/Chapter%204%20-%20Mining%20LinkedIn.ipynb

##### Aplicação na base de dados

#Obtendo todos os cargos dos contatos
todos_cargos = conexoes['Position'].values
len(todos_cargos)

#Convertendo os cargos em um conjunto para eliminar duplicatas
todos_cargos = set(todos_cargos)
len(todos_cargos)

#Definindo o limite da distância Jaccard para formação dos clusters
limite = 0.3
clusters = {}

#Percorrendo cada cargo para verificar quais são similares o suficiente para formar um cluster
for cargo1 in todos_cargos:
  clusters[cargo1] = []
  for cargo2 in todos_cargos:
# Evitando a formação de clusters duplicados
    if cargo2 in clusters[cargo1] or cargo2 in clusters and cargo1 in clusters[cargo2]:
      continue


# Calculando a distância Jaccard entre os cargos
distancia = jaccard_distance(set(cargo1), set(cargo2))
if distancia <= limite:
  # Adicionando o cargo ao cluster
  clusters[cargo1].append(cargo2)
#Convertendo o dicionário de clusters em uma lista de clusters e removendo clusters com apenas um cargo
clusters = [clusters[cargo] for cargo in clusters if len(clusters[cargo]) > 1]
clusters, len(clusters)

#Percorrendo cada contato e imprimindo o cargo correspondente
for contato in range(0, len(conexoes)):
  print(conexoes['Position'][contato])

#Criando um dicionário de clusters com os contatos correspondentes a cada cargo
cluster_contatos = {}
for cluster in clusters:
#print(cluster)
  cluster_contatos[tuple(cluster)] = []
for contato in range(0, len(conexoes)):
  if conexoes['Position'][contato] in cluster:
    cluster_contatos[tuple(cluster)].append(conexoes['Full Name'][contato])

#Imprimindo o dicionário de clusters com os contatos correspondentes a cada cargo
cluster_contatos

# Importando a biblioteca HTML do IPython para exibição de HTML em notebooks
from IPython.core.display import HTML

# Loop pelos clusters de contatos
for cargos in cluster_contatos:
  
  # Criando uma string com os cargos presentes no cluster
  lista_cargos = 'Lista de cargos no grupo: ' + ', '.join(cargos)

  # Inicializando o conjunto de termos com as palavras do primeiro cargo
  termos = set(cargos[0].split())

  # Iterando pelos demais cargos do cluster
  for palavras in cargos:
    # Atualizando o conjunto de termos, fazendo a interseção com as palavras do cargo atual
    termos.intersection_update(set(palavras.split()))

  # Se não houver termos em comum entre os cargos, exibe uma mensagem específica
  if len(termos) == 0:
    termos = ['***Nenhum termo em comum****']
  
  # Criando uma string com os termos em comum entre os cargos
  termos_impressao = 'Termos comuns: ' + ', '.join(termos)

  # Exibindo o título com a lista de cargos
  display(HTML(f'<h3>{lista_cargos}</h3>'))

  # Exibindo os termos em comum
  display(HTML(f'<p>{termos_impressao}</p>'))

  # Exibindo uma linha separadora
  display(HTML(f'<p>{"-" * 70}</p>'))

  # Exibindo a lista de contatos pertencentes ao cluster
  display(HTML(f'<p><mark>{", ".join(cluster_contatos[cargos])}</mark></p>'))

  
  #print(lista_cargos)
  #print('\n' + termos_impressao)
  #print('-' * 70)
  #print('\n'.join(cluster_contatos[cargos]))
  #print()