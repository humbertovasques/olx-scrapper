# Descripton: Web Scraper made to collect data from OlX about apartments for sale
# Author: Humberto Vasques

import requests
from bs4 import BeautifulSoup
import csv

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}

# Creating the data file
fileName = 'dataFile.csv'
firstLine = ['Título','Preço','Taxa de Condomínio','IPTU','Área','Banheiros','Vagas na Garagem','Detalhes do Imóvel','Detalhes do Condominio','CEP','Município','Bairro','Logradouro','Quartos']
with open(fileName,"w",newline="",encoding='UTF-8') as f:
        writer = csv.writer(f,delimiter=';')
        writer.writerow(firstLine)

# 100 pages ~ 5000 samples
numPages = 100

# Loop for search page
for page in range(1,numPages+1):

        searchUrl = f'https://rn.olx.com.br/rio-grande-do-norte/natal/imoveis/venda/apartamentos?o={page}'
        searchPage = requests.get(searchUrl, headers=headers)
        soup = BeautifulSoup(searchPage.content,'html.parser')
        
        # Loop for the ads in each page
        for link in soup.find_all('a',class_='sc-12rk7z2-1 huFwya sc-giadOv dXANPZ'):

                maxAtempts = 10
                atempt = 0
                while atempt < maxAtempts:

                        try:
                                adsLink = link.get('href') 
                                adsPage = requests.get(adsLink,headers=headers)
                                adsSoup = BeautifulSoup(adsPage.content,'html.parser')
                                
                                # List to save the data gathered
                                line = []
                                for l in range(14):line.append('empty')

                                # Data Scraping
                                # The code was written to extract the data as clean as possible.

                                line[0] = adsSoup.find('h1', class_ = 'sc-45jt43-0 eCghYu sc-ifAKCX cmFKIN').get_text().strip()
                                        
                                line[1] = adsSoup.find('h2', class_ = 'sc-1wimjbb-1 bQzdqU sc-ifAKCX cmFKIN').get_text().strip().split()[1].replace('.','')
                                
                                # The data below all have the same class, so I made a loop going through all of them, checking the text of the parent tag.
                                for kaNiaQ in adsSoup.find_all('dd', class_ = 'sc-1f2ug0x-1 ljYeKO sc-ifAKCX kaNiaQ'):
                                        
                                        if (kaNiaQ.parent.text.find('CondomínioR$') != -1):
                                                line[2] = kaNiaQ.parent.text.split()[1].replace('.','')
                                                
                                        if (kaNiaQ.parent.text.find('IPTUR$') != -1):
                                                line[3] = kaNiaQ.parent.text.split()[1].replace('.','')
                                                
                                        if (kaNiaQ.parent.text.find('Área útil') != -1):
                                                line[4] = kaNiaQ.parent.text.strip()[len('Área útil'):-2]
                                                
                                        if (kaNiaQ.parent.text.find('Banheiros') != -1):
                                                line[5] = kaNiaQ.parent.text.strip()[len('Banheiros'):]
                                                
                                        if (kaNiaQ.parent.text.find('Vagas na garagem') != -1):
                                                line[6] = kaNiaQ.parent.text.strip()[len('Vagas na garagem'):]
                                                
                                        if (kaNiaQ.parent.text.find('Detalhes do imóvel') != -1):
                                                line[7] = kaNiaQ.parent.text.strip()[len('Detalhes do imóvel'):]
                                                
                                        if (kaNiaQ.parent.text.find('Detalhes do condominio') != -1):
                                                line[8] = kaNiaQ.parent.text.strip()[len('Detalhes do condominio'):]
                                                
                                        if (kaNiaQ.parent.text.find('CEP') != -1):
                                                line[9] = kaNiaQ.parent.text.strip()[len('CEP'):]
                                                
                                        if (kaNiaQ.parent.text.find('Município') != -1):
                                                line[10] = kaNiaQ.parent.text.strip()[len('Município'):]
                                                
                                        if (kaNiaQ.parent.text.find('Bairro') != -1):
                                                line[11] = kaNiaQ.parent.text.strip()[len('Bairro'):]
                                        
                                        if (kaNiaQ.parent.text.find('Logradouro') != -1):
                                                line[12] = kaNiaQ.parent.text.strip()[len('Logradouro'):]

                                for dBeEuJ in adsSoup.find_all('a', class_ = 'sc-57pm5w-0 sc-1f2ug0x-2 dBeEuJ'):

                                        if (dBeEuJ.parent.text.find('Quartos') != -1):
                                                line[13] = dBeEuJ.parent.text.strip()[len('Quartos'):]

                                print('\npage:',page)
                                print(line)

                                # Saving the data gathered
                                with open(fileName,"a",newline="",encoding='UTF-8') as f:
                                        writer = csv.writer(f,delimiter=';')
                                        writer.writerow(line)
                        except:
                                atempt += 1 
                                continue
                        break