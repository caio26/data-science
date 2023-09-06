# Imports
import re
import bs4
import time
import json
import requests  
import pandas as pd
from bs4 import BeautifulSoup as bs


def InfoGeral(soup):
    # Encontra a tabela que contém informações gerais da série
    information = soup.find('table')
    side_info_par = []
    for info in information:
        # Filtra as informações que possuem mais de um caractere
        if len(info.text) > 1:
            # Limpa os caracteres de quebra de linha e espaços em branco
            info=info.text
            side_info_par.append(info.replace("\n", "").replace("  ", ""))
    return side_info_par

def OndeAssistir(soup):
    # Encontra os links para assistir a série
    onde_assistir = soup.find_all(attrs={"affiliate": True})
    where_watch = []
    for i in onde_assistir:
        # Obtém apenas o nome do serviço de streaming
        i=i.get("affiliate")
        where_watch.append(i)
    return where_watch

def nomes_atores(soup):
    # Encontra o elenco da série
    atores_ = soup.find_all(class_="tv-series__series-info-castCrew")
    atores=[]
    for x in atores_:
        # Limpa os caracteres de quebra de linha e espaços em branco
        x=x.text
        atores.append(x.replace("\n", "").replace("  ", ""))
    return atores

def sinopse_serie(soup):
    # Encontra a sinopse da série
    sinopse_ = soup.find(class_="tv-series__series-info--synopsis clamp clamp-6 js-clamp clearfix")
    sinopse=sinopse_.text
    return sinopse

def pegar_notas(soup):
    # Encontra as notas da série na crítica e no público
    rating_ = soup.find_all(class_="mop-ratings-wrap__percentage")
    rating = []
    for x in rating_:
        # Limpa os caracteres de quebra de linha e espaços em branco
        x=x.text
        try:
            # Tenta separar as notas da crítica e do público
            rating = [f'as notas da serie são: {rating} a nota da crítica ({rating[0]}) e a nota do público({rating[1]}']
        except:
            # Se não conseguir, adiciona apenas a nota encontrada
            rating.append(x.replace("\n", "").replace("  ", ""))
    return rating

def title_name(soup):
    # Encontra o título da página da série
    title_ = soup.find('title')
    title=[]
    for x in title_:
        # Remove o sufixo " - IMDb" do título
        x=x.text
        x=re.sub(r'\-.*', '', x)
        title.append(x) 
    return title
    
# Lista para os links
links = []
# URL
#30 links por pagina,estamos usnado 5 paginas = 150
url = f"https://www.rottentomatoes.com/browse/tv_series_browse/?page=6"
    
 # Request
rq = requests.get(url)
print(rq.status_code)
    
# Parse do html
soup = bs(rq.text, "html.parser")
    
 # Seleção do que desejamos
listsofA = soup.select(".js-tile-link")
    
# Loop para extrair o atributo href da tag a
for a in listsofA:
    links.append(a.get("href"))

links = [x for x in links if str(x) != 'None']

#criandp uma lista para concatenar o "https://www.imdb.com" + "links"
links_completos=[]

for link in links:
    concat='https://www.rottentomatoes.com' +link
    links_completos.append(concat)
        


 # O loop abaixo faz a leitura dos arquivos txt extraídos no loop anterior 
 # e aplica as funções de web scraping para extrair os dados de cada link. 
 # Os resultados de cada página são salvos em arquivos txt.



    
# Leitura dos arquivos txt com os links
with open(f"D:\webscraping\links_filmes_rotten.txt", "r") as file:
    links = file.readlines()
    links = [line.rstrip() for line in links]

#lista
seriesInfo=[]

# Request para cada link
for link in links:
    print(link)

    #exemplo:https://www.rottentomatoes.com/tv/the_last_of_us
    rq = requests.get(link)
        
    # Soup com parse do html
    soup = bs(rq.text, "html.parser") 
               
     # Extrai os dados e salva na lista no formato de dicionário
    seriesInfo.append(dict( 
        nome                     = title_name(soup),
        infoGeral                = InfoGeral(soup),
        notas                    = pegar_notas(soup),
        nomeAtores               = nomes_atores(soup),
        aonde_assistir           = OndeAssistir(soup),
        sinopse                  = sinopse_serie(soup))),
        
        # Sleep
    time.sleep(5)

    # Grava o resultado em disco
    with open(f"D:\webscraping\seriesInfo", 'w') as fout:
        json.dump(seriesInfo, fout)
           
    # Sleep
    time.sleep(10)

    with open('seriesInfo','r') as a:
        data = json.load(a)

#O arquivo e do tipo(lista)
print(type(data))
