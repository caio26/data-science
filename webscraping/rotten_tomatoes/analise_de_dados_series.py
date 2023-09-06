import dataframe_series
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

df=dataframe_series.df6.copy()

# Substitui valores 'nan' pela representação de NaN do numpy
df.notas_do_publico.replace('nan', np.nan, inplace=True)
df.notas_da_critica.replace('nan', np.nan, inplace=True)

# Converte as colunas 'notas_do_publico' e 'notas_da_critica' para valores numéricos, e trata erros com a opção 'coerce' para que valores inválidos sejam convertidos em NaN
df['notas_do_publico'] = pd.to_numeric(df['notas_do_publico'], errors='coerce')
df['notas_da_critica'] = pd.to_numeric(df['notas_da_critica'], errors='coerce') 

# Define a função media_notas que recebe uma linha do DataFrame como parâmetro
def media_notas(row):
    notas_sem_nan = []
    # Itera sobre as notas do público e da crítica, verificando se há valores nulos
    for nota in ['notas_do_publico', 'notas_da_critica']:
        if pd.isna(row[nota]):
            # Caso haja valores nulos, retorna um valor indicando que há valores insuficientes para cálculo da média
            return 'valores_insuficientes'
        notas_sem_nan.append(row[nota])
    # Calcula a média das notas sem valores nulos
    return np.mean(notas_sem_nan)


# Cria uma nova coluna 'media_notas' no DataFrame df, aplicando a função media_notas em cada linha
df['media_notas'] = df.apply(media_notas, axis=1)

# Cria um novo DataFrame df2, que contém apenas as linhas que não possuem valores insuficientes para cálculo da média das notas
df2 = df[df['media_notas'] != 'valores_insuficientes']

# converte a coluna de notas para valores numéricos
df2['media_notas'] = pd.to_numeric(df2['media_notas'])

# Plota o primeiro gráfico no primeiro subplot
# Seleciona os 15 séries com as maiores médias de notas
df2_top_15_media_notas = df2.sort_values(by='media_notas', ascending=False).head(15)
# Seleciona as 25 séries com as maiores notas da crítica
df2_top_25_nota_da_critica = df2.sort_values(by='notas_da_critica', ascending=False).head(25)
# Seleciona as top 15 séries com notas do público mais altas
df2_top_15_nota_do_publico = df2.sort_values(by='notas_do_publico', ascending=False).head(15)


colors = ['#ff7f0e', '#1f77b4', '#2ca02c']
# Define o estilo do Seaborn

sns.set_style('whitegrid')
# Cria a figura e os subplots

fig, axs = plt.subplots(3, figsize=(20,35))
# Plota o primeiro gráfico no primeiro subplot

sns.barplot(ax=axs[0], x='nome', y='media_notas', data=df2_top_15_media_notas, color=colors[0])
axs[0].set_title('Média das Notas por série', fontsize=26, fontweight='bold')
axs[0].set_ylabel('Média das Notas', fontsize=12)
axs[0].set_ylim(90, 100)
axs[0].tick_params(axis='x', labelsize=20, rotation=80, labelcolor='black')
axs[0].tick_params(axis='y', labelsize=22, labelcolor='gray')
# Plota o segundo gráfico no segundo subplot

sns.barplot(ax=axs[1], x='nome', y='notas_da_critica', data=df2_top_25_nota_da_critica, color=colors[1])
axs[1].set_title('Notas da Crítica por série', fontsize=26, fontweight='bold')
axs[1].set_ylabel('Notas da Crítica', fontsize=12)
axs[1].set_ylim(90, 100)
axs[1].tick_params(axis='x', labelsize=20, rotation=80, labelcolor='black')
axs[1].tick_params(axis='y', labelsize=22, labelcolor='gray')
# Plota o terceiro gráfico no terceiro subplot

sns.barplot(ax=axs[2], x='nome', y='notas_do_publico', data=df2_top_15_nota_do_publico, color=colors[2])
axs[2].set_title('Notas do Público por série', fontsize=26, fontweight='bold')
axs[2].set_ylabel('Notas do Público', fontsize=12)
axs[2].set_ylim(90, 100)
axs[2].tick_params(axis='x', labelsize=20, rotation=80, labelcolor='black')
axs[2].tick_params(axis='y', labelsize=22, labelcolor='gray')
fig.subplots_adjust(hspace=1.0)
# Define as legendas para cada subplot e ajusta o tamanho e espaçamento

legend1 = axs[0].legend(['Média das Notas'], loc='upper left', prop={'size': 15}, borderpad=1)
legend2 = axs[1].legend(['Notas da Crítica'], loc='upper left', prop={'size': 15}, borderpad=1)
legend3 = axs[2].legend(['Notas do Público'], loc='upper center', prop={'size': 15}, borderpad=1)

df2_top_15_media_notas_por_genero =df2_top_15_media_notas['Genero'].value_counts()
# Cria o countplot utilizando o Seaborn
sns.countplot(data=df2_top_15_media_notas, x='Genero')

# Define o label do eixo y
plt.ylabel('Quantidade de Séries')

# Adiciona um título ao gráfico
plt.title('Quantidade dos Generos das séries presentes no top 15')

# Verifica quantas séries do top 25 da nota da crítica não estão nas top 15 do público
not_in_publico = df2_top_25_nota_da_critica[~df2_top_25_nota_da_critica['nome'].isin(df2_top_15_nota_do_publico['nome'])]
print(f"{len(not_in_publico)} séries do top 25 da nota da crítica não estão nas top 15 do público.")

# Imprime o nome das séries que não estão no top do público
print("Séries do top da crítica que não estão no top do público:")
print(not_in_publico['nome'].values)

# Conta quantos programas cada rede de TV tem
séries_publico_critica = df2.groupby("nome").agg({'notas_do_publico': 'mean', 'notas_da_critica': 'mean'}).reset_index()
# Calcula a diferença entre as notas do público e da crítica para cada rede de TV
séries_publico_critica['publico-critica'] = séries_publico_critica['notas_do_publico']-séries_publico_critica['notas_da_critica']

# Ordena as séries de TV pela diferença entre as notas do público e da crítica, em ordem decrescente
séries_publico_critica = séries_publico_critica.sort_values(by='publico-critica', ascending=False)

#selecionando as 15 séries de TV com a maior diferença entre a nota do público e a nota da crítica
séries_publico_critica=séries_publico_critica.tail(15)

#criando gráfico de barras

plt.figure(figsize=(15, 15))
sns.barplot(x='nome',y='publico-critica',data=séries_publico_critica)

# definindo o título do gráfico
plt.title('diferença entre a média de nota do público e a diferença da nota média da critica entre séries ', fontsize=22, fontweight='bold')

# definindo o limite superior do eixo y
plt.ylim(0, -50)

# definindo o tamanho das labels do eixo x
plt.tick_params(axis='x', labelsize=22, rotation=80)

# definindo o tamanho das labels do eixo y
plt.tick_params(axis='y', labelsize=15)

# exibindo o gráfico
plt.show()

# Conta quantos programas cada rede de TV tem.
Tv_network_counts = df2['Tv_network'].value_counts()

# Calcula a média das notas para cada rede de TV
df2_nota_tv_network = df2.groupby('Tv_network')['media_notas'].mean().reset_index()

# Considera apenas as redes de TV que possuem mais de 5 programas avaliados
df2_nota_tv_network = df2_nota_tv_network[Tv_network_counts[df2_nota_tv_network['Tv_network']].values >= 5]

# Plota o primeiro gráfico
fig, axs = plt.subplots(3, figsize=(8,12))
axs[0].plot(df2_nota_tv_network['Tv_network'], df2_nota_tv_network['media_notas'], marker='o')
axs[0].scatter(df2_nota_tv_network['Tv_network'], df2_nota_tv_network['media_notas'], color='black')
axs[0].set_xticklabels(axs[0].get_xticklabels(), rotation=65, ha='right')
axs[0].set_title('Média das Notas por Rede de TV')
axs[0].set_ylim(60, 100)

# Calcula a média das notas da crítica para cada rede de TV
df2_nota_critica_tv_network = df2.groupby('Tv_network')['notas_da_critica'].mean().reset_index()

# Considera apenas as redes de TV que possuem mais de 5 programas avaliados
df2_nota_critica_tv_network = df2_nota_critica_tv_network[Tv_network_counts[df2_nota_critica_tv_network['Tv_network']].values >= 5]

# Plota o segundo gráfico
axs[1].plot(df2_nota_critica_tv_network['Tv_network'], df2_nota_critica_tv_network['notas_da_critica'], marker='o')
axs[1].scatter(df2_nota_critica_tv_network['Tv_network'], df2_nota_critica_tv_network['notas_da_critica'], color='black')
axs[1].set_xticklabels(axs[1].get_xticklabels(), rotation=65, ha='right')
axs[1].set_title('Média das Notas da crítica por Rede de TV')
axs[1].set_ylim(60, 100)

# Calcula a média das notas do público para cada rede de TV
df2_nota_publico_tv_network = df2.groupby('Tv_network')['notas_do_publico'].mean().reset_index()

# Considera apenas as redes de TV que possuem mais de 5 programas avaliados
df2_nota_publico_tv_network = df2_nota_publico_tv_network[Tv_network_counts[df2_nota_publico_tv_network['Tv_network']].values >= 5]

# Plota o terceiro grafico

axs[2].plot(df2_nota_publico_tv_network['Tv_network'], df2_nota_publico_tv_network['notas_do_publico'], marker='o')
axs[2].scatter(df2_nota_publico_tv_network['Tv_network'], df2_nota_publico_tv_network['notas_do_publico'], color='black')
axs[2].set_xticklabels(axs[2].get_xticklabels(), rotation=65, ha='right')
axs[2].set_title('Média das Notas do público por Rede de TV')
axs[2].set_ylim(60, 100)

#Adiciona espaço entre os gráficos
plt.subplots_adjust(hspace=0.7)

plt.show()


# Agrupa as notas médias do público e da crítica por rede de TV e seleciona apenas as redes com mais de 5 séries avaliadas
Tv_network_publico_critica = df2.groupby("Tv_network").agg({'notas_do_publico': 'mean', 'notas_da_critica': 'mean'}).reset_index()
Tv_network_publico_critica = Tv_network_publico_critica[Tv_network_counts[Tv_network_publico_critica['Tv_network']].values >= 5]

# Calcula a diferença entre as notas do público e da crítica para cada rede de TV
Tv_network_publico_critica['publico-critica'] = Tv_network_publico_critica['notas_do_publico']-Tv_network_publico_critica['notas_da_critica']

# Ordena as redes de TV pela diferença entre as notas do público e da crítica, em ordem decrescente
Tv_network_publico_critica = Tv_network_publico_critica.sort_values(by='publico-critica', ascending=False)

# Cria um gráfico de barras com as diferenças entre as notas do público e da crítica para cada rede de TV
plt.figure(figsize=(18, 15))
sns.barplot(x='Tv_network',y='publico-critica',data=Tv_network_publico_critica)

# Define o título do gráfico e limites para o eixo y
plt.title('diferença entre a média de nota do público e a diferença da nota do ', fontsize=22, fontweight='bold')
plt.ylim(-15, 10)

# Define o tamanho da fonte para as labels do eixo x e exibe o gráfico
plt.tick_params(axis='x', labelsize=22)
plt.show()


# Define a figura principal e seus subplots
fig, axs = plt.subplots(3, figsize=(20,35))

# Define as cores dos gráficos
colors = ['#ff7f0e', '#1f77b4', '#f7b6d2'] 

# Define o estilo do grid
sns.set_style('whitegrid')

# Conta a quantidade de séries por gênero
genero_count=df2.Genero.value_counts()

# Agrupa o dataframe por gênero e calcula a média das notas
df2_genero_media_notas = df2.groupby("Genero")['media_notas'].mean().reset_index()
# Filtra os gêneros que possuem mais de 4 Séries
df2_genero_media_notas =df2_genero_media_notas[genero_count[df2_genero_media_notas['Genero']].values >= 4]

# Cria o primeiro subplot com o gráfico de barras da média das notas por gênero
sns.barplot(ax=axs[0], x='Genero', y='media_notas', data=df2_genero_media_notas,color=colors[0])
axs[0].set_title('Média das Notas por gênero', fontsize=26, fontweight='bold')
axs[0].set_ylabel('Média das Notas', fontsize=12)
axs[0].set_ylim(60, 100)
axs[0].tick_params(axis='x', labelsize=20, rotation=0, labelcolor='black')
axs[0].tick_params(axis='y', labelsize=22, labelcolor='gray')

# Agrupa o dataframe por gênero e calcula a média das notas da crítica
df2_genero_notas_critica= df2.groupby("Genero")['notas_da_critica'].mean().reset_index()
# Filtra os gêneros que possuem mais de 4 series
df2_genero_notas_critica = df2_genero_notas_critica[genero_count[df2_genero_notas_critica['Genero']].values >= 4]

# Cria o segundo subplot com o gráfico de barras das notas da crítica por gênero
sns.barplot(ax=axs[1], x='Genero', y='notas_da_critica', data=df2_genero_notas_critica, color=colors[1])
axs[1].set_title('Notas da Crítica por gênero', fontsize=26, fontweight='bold')
axs[1].set_ylabel('Notas da Crítica', fontsize=12)
axs[1].set_ylim(60, 100)
axs[1].tick_params(axis='x', labelsize=20, rotation=0, labelcolor='black')
axs[1].tick_params(axis='y', labelsize=22, labelcolor='gray')

# Agrupa o dataframe por gênero e calcula a média das notas do público
df2_genero_notas_publico= df2.groupby("Genero")['notas_do_publico'].mean().reset_index()
# Filtra os gêneros que possuem mais de 4 séries
df2_genero_notas_publico = df2_genero_notas_publico[genero_count[df2_genero_notas_publico['Genero']].values >= 4]

sns.barplot(ax=axs[2], x='Genero', y='notas_do_publico', data=df2_genero_notas_publico, color=colors[2])
axs[2].set_title('Notas do Público por gênero', fontsize=26, fontweight='bold')
axs[2].set_ylabel('Notas do Público', fontsize=12)
axs[2].set_ylim(60, 100)
axs[2].tick_params(axis='x', labelsize=20, rotation=0, labelcolor='black')
axs[2].tick_params(axis='y', labelsize=22, labelcolor='gray')
fig.subplots_adjust(hspace=1.0)


legend1 = axs[0].legend(['Média das Notas'], loc='upper left', prop={'size': 15}, borderpad=1)
legend2 = axs[1].legend(['Notas da Crítica'], loc='upper left', prop={'size': 15}, borderpad=1)
legend3 = axs[2].legend(['Notas do Público'], loc='upper center', prop={'size': 15}, borderpad=1)

plt.show()

# agrupando o dataset pela coluna "Genero" e calculando a média das colunas "notas_do_publico" e "notas_da_critica"
genero_publico_critica = df2.groupby("Genero").agg({'notas_do_publico': 'mean', 'notas_da_critica': 'mean'}).reset_index()

# filtrando os dados para manter apenas os gêneros com pelo menos 4 ocorrências
genero_publico_critica = genero_publico_critica[genero_count[genero_publico_critica['Genero']].values >= 4]

# criando uma nova coluna "publico-critica" com a diferença entre as médias das colunas "notas_do_publico" e "notas_da_critica"
genero_publico_critica['publico-critica'] = genero_publico_critica['notas_do_publico']-genero_publico_critica['notas_da_critica']

# ordenando o dataframe pela coluna "publico-critica" de forma decrescente
genero_publico_critica = genero_publico_critica.sort_values(by='publico-critica', ascending=False)

# criando um gráfico de barras usando seaborn com os valores de "Genero" no eixo x e os valores de "publico-critica" no eixo y
plt.figure(figsize=(15, 15))
sns.barplot(x='Genero',y='publico-critica',data=genero_publico_critica)

# definindo o título do gráfico
plt.title('diferença entre a média de nota do público e a diferença da critica por genero', fontsize=26, fontweight='bold')

# definindo o limite superior do eixo y
plt.ylim(0, -20)

# definindo o tamanho das labels do eixo x
plt.tick_params(axis='x', labelsize=22)

# exibindo o gráfico
plt.show()

# Criando um scatter plot
plt.scatter(df2["notas_da_critica"], df2["notas_do_publico"])

# Adicionando rótulos e título
plt.xlabel("Nota da crítica")
plt.ylabel("Nota do público")
plt.title("Correlação das notas da crítica e do público")

# Exibindo o gráfico
plt.show()

# Seleciona apenas as colunas de interesse
atores = df2[['ator_1', 'ator_2', 'ator_3', 'ator_4', 'ator_5']]

# Conta a frequência de cada ator em todas as colunas de atores
contagem_atores = atores.stack().value_counts()

# Filtra apenas os atores que aparecem pelo menos duas vezes
atores_relevantes = contagem_atores.loc[contagem_atores >= 2].index.tolist()

# Cria uma lista para armazenar as informações de cada ator encontrado
lista_info_atores = []

# Loop pelos atores relevantes
for ator in atores_relevantes:
    # Filtra o dataframe apenas para as linhas em que o ator aparece
    df_ator = df2.loc[(df2['ator_1'] == ator) | (df2['ator_2'] == ator) | (df2['ator_3'] == ator) | (df2['ator_4'] == ator) | (df2['ator_5'] == ator)]
    # Loop pelas séries em que o ator aparece
    for _, row in df_ator.iterrows():
        # Extrai as informações desejadas para cada linha correspondente ao ator
        nome_serie = row['nome']
        nota_critica = row['notas_da_critica']
        nota_publico = row['notas_do_publico']
        media_notas =  row['media_notas']
        # Adiciona as informações na lista de informações de atores
        lista_info_atores.append([nome_serie, ator, nota_critica, nota_publico,media_notas])

# Cria um dataframe a partir da lista de informações de atores
df_atores = pd.DataFrame(lista_info_atores, columns=['Nome da série', 'Ator', 'Nota da crítica', 'Nota do público','media_notas'])

# Exibe o dataframe com as informações de atores encontrados
df_atores


#Agrupa os dados da tabela "df_atores" pela coluna "Ator" e calcula a média das notas para cada ator
df_atores_media_notas = df_atores.groupby("Ator")['media_notas'].mean().reset_index()

#Ordena a tabela em ordem decrescente com base na coluna "media_notas"
df_atores_media_notas = df_atores_media_notas.sort_values(by='media_notas', ascending=False)

plt.figure(figsize=(15, 8))  # Define o tamanho da figura
plt.scatter(x='Ator', y='media_notas', data=df_atores_media_notas)  # Plota o scatterplot
plt.plot(df_atores_media_notas['Ator'], df_atores_media_notas['media_notas'], color='red', linestyle='--')  # Adiciona a linha vermelha pontilhada
plt.title('Média das notas por ator', fontsize=16)  # Adiciona o título
plt.xlabel('Ator', fontsize=12)  # Adiciona o label do eixo x
plt.ylabel('Média das notas', fontsize=12)  # Adiciona o label do eixo y
plt.xticks(rotation=45)  # Altera a rotação do eixo x para 45 graus
plt.ylim(40, 100)  # Define os limites do eixo y
plt.show()  # Mostra o gráfico

# Agrupa o dataframe df_atores pela coluna "Ator" e calcula a média da coluna "Nota da crítica"
df_atores_nota_critica = df_atores.groupby("Ator")['Nota da crítica'].mean().reset_index()
# Ordena o dataframe df_atores_nota_critica em ordem decrescente pela coluna "Nota da crítica"
df_atores_nota_critica = df_atores_nota_critica.sort_values(by='Nota da crítica', ascending=False)

plt.figure(figsize=(15, 8))  # Define o tamanho da figura
plt.scatter(x='Ator', y='Nota da crítica', data=df_atores_nota_critica)  # Plota o scatterplot
plt.plot(df_atores_nota_critica['Ator'], df_atores_nota_critica['Nota da crítica'], color='red', linestyle='--')  # Adiciona a linha vermelha pontilhada
plt.title('Média das notas da critica por ator', fontsize=16)  # Adiciona o título
plt.xlabel('Ator', fontsize=12)  # Adiciona o label do eixo x
plt.ylabel('Média das notas', fontsize=12)  # Adiciona o label do eixo y
plt.xticks(rotation=45)  # Altera a rotação do eixo x para 45 graus
plt.ylim(40, 100)  # Define os limites do eixo y
plt.show()  # Mostra o gráfico


# Agrupa por ator e calcula a média da nota do público
df_atores_nota_publico = df_atores.groupby("Ator")['Nota do público'].mean().reset_index()

# Ordena em ordem decrescente pela nota do público
df_atores_nota_publico = df_atores_nota_publico.sort_values(by='Nota do público', ascending=False)

plt.figure(figsize=(15, 8))  # Define o tamanho da figura
plt.scatter(x='Ator', y='Nota do público', data=df_atores_nota_publico)  # Plota o scatterplot
plt.plot(df_atores_nota_publico['Ator'], df_atores_nota_publico['Nota do público'], color='red', linestyle='--')  # Adiciona a linha vermelha pontilhada
plt.title('Média das notas do pblico por ator', fontsize=16)  # Adiciona o título
plt.xlabel('Ator', fontsize=12)  # Adiciona o label do eixo x
plt.ylabel('Média das notas', fontsize=12)  # Adiciona o label do eixo y
plt.xticks(rotation=45)  # Altera a rotação do eixo x para 45 graus
plt.ylim(40, 100)  # Define os limites do eixo y
plt.show()  # Mostra o gráfico

