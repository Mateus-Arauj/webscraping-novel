import requests 
from bs4 import BeautifulSoup
from tqdm import tqdm 


url = 'https://novelmania.com.br'

print("Insira a url da novel:")
entrada = input()
print("Insira o nome da novel:")
nome_novel = input()
response = requests.get(entrada)

content = response.content
soup = BeautifulSoup(content, 'html.parser')

card = soup.find_all('ol',{'class': "list-inline"})

for i in tqdm(card):
    ilist = i.find_all('li')
    for li in ilist:
        r = li.find('a')
        webscrap = requests.get(url + r['href'])
        soup = BeautifulSoup(webscrap.content, 'html.parser')
        result = soup.find('div',{'class': 'text'})
        text_file = open("livro.txt", "a")
        n = text_file. write(result.text)
        text_file. close()
    