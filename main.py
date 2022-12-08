import requests 
from bs4 import BeautifulSoup
from tqdm import tqdm 
import pypub
import urllib.request
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import os

print("Insira a url da novel:")
entrada = input()
print("Insira o nome da novel:")
nome_novel = input()
options = Options()
options.headless = True



driver = webdriver.Firefox(options= options)
driver.maximize_window()
driver.get(entrada)
driver.find_element(By.CLASS_NAME, "btn-reverse-order").click()
pageSource = driver.page_source
driver.quit()

soup = BeautifulSoup(pageSource, 'html.parser')
imgUrl = soup.find('div', {'class': 'summary_image'})
imgUrl = imgUrl.find('img')['data-src']
urllib.request.urlretrieve(imgUrl, f"imgs/{nome_novel}.jpg")
card = soup.find("div", {"id": "manga-chapters-holder"})
card = soup.find("ul", {"class": "main version-chap active"})
card = soup.find_all("li", {"class": "wp-manga-chapter"})
my_first_epub = pypub.Epub(nome_novel, cover = f'imgs/{nome_novel}.jpg')


for i in tqdm(card, unit = "Cap"):
    r = i.find('a')
    webscrap = requests.get(r['href'])
    soup = BeautifulSoup(webscrap.content, 'html.parser')
    result = soup.find('div',{'class': 'text-left'})
    title = r.text
    #print(title)
    #print(result.text)
    c = pypub.create_chapter_from_string(result,title=title)
    my_first_epub.add_chapter(c)

my_first_epub.create_epub(os.getcwd()+'/ebooks')