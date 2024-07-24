import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

# Define the path to the Chrome driver
#chrome_driver_path = "C:\\Windows\\chromedriver.exe"

###Embrapa###

# Cria uma nova instância do navegador Chrome
browser = webdriver.Chrome()
# Navega para o site que você deseja raspar
url = "https://www.embrapa.br/"
browser.get(url)
# Analisa o conteúdo HTML usando BeautifulSoup
soup = BeautifulSoup(browser.page_source, 'html.parser')
# Encontra os elementos que você deseja extrair
elements = soup.find_all('div', class_='tp-card-corpo')
with open("embrapa.xml", "w", encoding='utf-8') as arq:
    for element in elements:
        arq.write(element.get_text() + "\n")
# Extrai os dados dos elementos
data = [element.get_text() for element in elements]
# Imprime os dados extraídos
for item in data:
    print(item)
    
# Cria o arquivo CSV e escreve os dados nele
with open("embrapa.csv", "w", newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=' ')
    
    # Escreve o cabeçalho do CSV
    csvwriter.writerow(['Tag', 'Titulo', 'Descricao'])
    
    for element in elements:
        # Verifica se os elementos existem antes de tentar extrair o texto
        tag = element.find('div', class_='tp-card-tag')
        titulo = element.find('h4', class_='tp-card-titulo')
        descricao = element.find('div', class_='tp-card-descricao')
        
        # Extrai o texto ou define como 'N/A' se não encontrado
        tag_text = tag.get_text().strip() if tag else ''
        titulo_text = titulo.get_text().strip() if titulo else ''
        descricao_text = descricao.get_text().strip() if descricao else ''
        
        # Escreve o texto no arquivo CSV como uma nova linha
        csvwriter.writerow([tag_text, titulo_text, descricao_text])
            
# Fecha o navegador
browser.quit()

###Agrofy###

browser = webdriver.Chrome()
url = "https://news.agrofy.com.br/cotacoes"
browser.get(url)
soup = BeautifulSoup(browser.page_source, 'html.parser')
elements = soup.find_all('table', class_='table-agrofy table')
with open("agrofy.xml", "w", encoding='utf-8') as arq:
    for element in elements:
        arq.write(element.get_text() + "\n")
data = [element.get_text() for element in elements]
for item in data:
    print(item)
    
    # Cria o arquivo CSV e escreve os dados nele
with open("agrofy.csv", "w", newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=' ')
    
    for element in elements:
        rows = element.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            data = [col.get_text().strip() for col in cols]
            csvwriter.writerow(data)
            
browser.quit()

###NoticiasAgricolas###

browser = webdriver.Chrome()
url = "https://www.noticiasagricolas.com.br/cotacoes/"
browser.get(url)
soup = BeautifulSoup(browser.page_source, 'html.parser')
elements = soup.find_all('div', class_='cotacao')
with open("noticiasagricolas.xml", "w", encoding='utf-8') as arq:
    for element in elements:
        arq.write(element.get_text() + "\n")
data = [element.get_text() for element in elements]
for item in data:
    print(item)
    
    
    
    
    
    
    
# Cria o arquivo CSV e escreve os dados nele
with open("noticiasagricolas.csv", "w", newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=' ')
    
    # Escreve o cabeçalho do CSV
    csvwriter.writerow(['Comoditie', 'Indicador', 'Fonte', 'Data', 'Valor', 'Variacao'])
    
    for element in elements:
        # Verifica se os elementos existem antes de tentar extrair o texto
        comoditie = element.find('a', 'title')
        indicador = element.find('h2')
        fonte = element.find('span')
        
        rows = element.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:
                data = cols[0].get_text().strip()
                valor = cols[1].get_text().strip()
                variacao = cols[2].get_text().strip()
                
        
        # Extrai o texto ou define como 'N/A' se não encontrado
        comoditie_text = comoditie.get_text().strip() if comoditie else ''
        indicador_text = indicador.get_text().strip() if indicador else ''
        fonte_text = fonte.get_text().strip() if fonte else ''
        
        # Escreve o texto no arquivo CSV como uma nova linha
        csvwriter.writerow([comoditie_text, indicador_text, fonte_text, data, valor, variacao])
        
browser.quit()

###AgroMeteorologia###

# Inicia uma instância do navegador Chrome
browser = webdriver.Chrome()
# Define a URL do site que será acessado
url = "http://200.201.27.34/agrometeorologia/mapasdiarios/mapa_precipitacao_.png"
# Acessa a URL especificada
browser.get(url)
# Obtém o conteúdo HTML da página acessada
soup = BeautifulSoup(browser.page_source, 'html.parser')
# Encontra todos os elementos <img> na página
elements = soup.find_all('img')
# Para cada elemento <img> encontrado
for element in elements:
    # Obtém o atributo 'src' do elemento <img>
    img_url = element.get('src')
    # Se o atributo 'src' existir
    if img_url:
        # Faz uma requisição HTTP GET para obter a imagem
        response = requests.get(img_url)
        # Se a requisição for bem-sucedida (código de status 200)
        if response.status_code == 200:
            # Abre um arquivo para escrever a imagem, nomeado com base no índice do elemento
            with open("image_{}.png".format(elements.index(element)), "wb") as f:
                # Escreve o conteúdo da resposta (a imagem) no arquivo
                f.write(response.content)
# Fecha o navegador
browser.quit()

###Agricultura.pr.gov.br###

browser = webdriver.Chrome()
url = "https://www.agricultura.pr.gov.br/Noticias"
browser.get(url)
soup = BeautifulSoup(browser.page_source, 'html.parser')
elements = soup.find_all('div', class_='item-news-content')
with open("agriculturaPrGovBr.xml", "w", encoding='utf-8') as arq:
    for element in elements:
        arq.write(element.get_text() + "\n")
data = [element.get_text() for element in elements]
for item in data:
    print(item)
browser.quit()
