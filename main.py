import requests 
from bs4 import BeautifulSoup
from tqdm import tqdm 
import pypub
import os

url = 'https://kiniga.com/'

print("Insira a url da novel:")
entrada = 'https://kiniga.com/projeto/os-contos-de-anima/'
print("Insira o nome da novel:")
nome_novel = 'Teste'

response = requests.get(entrada)

my_first_epub = pypub.Epub(nome_novel)

content = response.content
soup = BeautifulSoup(content, 'html.parser')
card = soup.find('div', {'class': 'listing-chapters_wrap show-more show'})
print(card)
# for i in tqdm(card):
#     print(i)
#     r = i.find('a')
#     webscrap = requests.get(r['href'])
#     soup = BeautifulSoup(webscrap.content, 'html.parser')
#     print(soup.prettify)
#     result = soup.find('div',{'class': 'text'})
#     title = result.find('h2')
#     print(title.text)
#     c = pypub.create_chapter_from_string(result,title=title.text)
#     my_first_epub.add_chapter(c)

# my_first_epub.create_epub(os.getcwd())