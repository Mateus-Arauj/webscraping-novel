import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pypub
import urllib.request
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import os
from ebooklib import epub
import threading
import queue

def kiniga():
    print("Insira a url da novel:")
    entrada = input()
    print("Insira o nome da novel:")
    nome_novel = input()
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
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
    my_first_epub = pypub.Epub(nome_novel, cover=f'imgs/{nome_novel}.jpg')

    for i in tqdm(card, unit="Cap"):
        r = i.find('a')
        webscrap = requests.get(r['href'])
        soup = BeautifulSoup(webscrap.content, 'html.parser')
        result = soup.find('div', {'class': 'text-left'})
        title = r.text
        # print(title)
        # print(result.text)
        c = pypub.create_chapter_from_string(result, title=title)
        my_first_epub.add_chapter(c)
    my_first_epub.create_epub(os.getcwd()+'/ebooks')


def saikaiscan():
    url = 'https://saikaiscan.com.br'
    print("Insira a url da novel:")
    entrada = 'https://saikaiscan.com.br/series/madan-no-ou-to-vanadis?tab=capitulos'
    print("Insira o nome da novel:")
    nome_novel = 'Madan no Ou to Vanadis'
    options = Options()
    #options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    driver.get(entrada)

    pageSource = driver.page_source
    soup = BeautifulSoup(pageSource, 'html.parser')
    imgUrl = soup.find('figure', {'class': 'image is-3by4 is-fullwidth'})
    imgUrl = imgUrl.find('img')['src']
    urllib.request.urlretrieve(imgUrl, f"imgs/{nome_novel}.jpg")

    volumesAction = driver.find_elements(By.CLASS_NAME, "active")
    volumes = []
    for volumeAction in volumesAction:
        volumeAction.click()
        volumes.append(driver.find_element(
            By.CLASS_NAME, "__chapters").get_attribute('innerHTML'))
    driver.quit()

    for volume in tqdm(volumes, unit="Vol"):
        soup = BeautifulSoup(volume, 'html.parser')
        soup = soup.find_all('li')
        book = epub.EpubBook()
        book.set_identifier("novel123456")
        book.set_title(f"{nome_novel}")
        book.set_language("en")
        book.add_author("NIELIF")
        for li in tqdm(soup, unit="Cap"):
            r = li.find('a')
            session = requests.Session()
            webscrap = session.get(url + r['href'])
            soup = BeautifulSoup(webscrap.content, 'html.parser')
            content = soup.find('div', {'class': ['__body', 'theme-2']})
            title = soup.find('h1')
            cap = epub.EpubHtml(
                title=title.text, file_name=f"{title.text}.xhtml", lang="en")
            cap.content = content.prettify()
            book.add_item(cap)
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        style = '''
                @namespace epub "http://www.idpf.org/2007/ops";
                body {
                    font-family: Cambria, Liberation Serif, Bitstream Vera Serif, Georgia, Times, Times New Roman, serif;
                }
                h2 {
                    text-align: left;
                    text-transform: uppercase;
                    font-weight: 200;     
                }
                ol {
                        list-style-type: none;
                }
                ol > li:first-child {
                        margin-top: 0.3em;
                }
                nav[epub|type~='toc'] > ol > li > ol  {
                    list-style-type:square;
                }
                nav[epub|type~='toc'] > ol > li > ol > li {
                        margin-top: 0.3em;
                }
                '''
        nav_css = epub.EpubItem(
            uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
        book.add_item(nav_css)
        book.add_item(nav_css)
        epub.write_epub("test.epub", book, {})


def reaperscans():
    print("Insira a url da novel:")
    entrada = 'https://reaperscans.net/series/o-comeco-apos-o-fim-novel-1681164000371'
    print("Insira o nome da novel:")
    nome_novel = input()
    const_name = 'https://reaperscans.net'
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    driver.get(entrada)
    pageSource = driver.page_source
    driver.quit()

    soup = BeautifulSoup(pageSource, 'html.parser')
    imgUrl = soup.find('div', {'class': 'sc-papXJ BBjVU'})
    imgUrl = imgUrl.find('img')['src']
    urllib.request.urlretrieve(imgUrl, f"imgs/{nome_novel}.jpg")
    card = soup.find_all("a", {"class": "c-jpNfKV"})
    my_first_epub = pypub.Epub(nome_novel, cover=f'imgs/{nome_novel}.jpg')
    card_inv = card[:: -1]
    card_inv = card_inv[389:]

    #Função para achar o cap
    # for i, ca in enumerate(card_inv):
    #     result = ca.find('span').text
    #     if result == "Capítulo 371":
    #         print(i)
    #         break
    #     print(result)


    # for i in tqdm(card_inv, unit="Cap"):
    #     r = i['href']
    #     print(const_name+r)
    #     options = Options()
    #     options.headless = True
    #     driver = webdriver.Firefox(options=options)
    #     driver.get(const_name + r)
    #     pageSource = driver.page_source
    #     driver.quit()
    #     soup = BeautifulSoup(pageSource, 'html.parser')
    #     result = soup.find('div', {'id': 'reading-content'})
    #     title = soup.find('title').text
    #     #print(title)
    #     print(result)
    #     c = pypub.create_chapter_from_string(result, title=title)
    #     my_first_epub.add_chapter(c)
    # my_first_epub.create_epub(os.getcwd()+'/ebooks')
    def processar_item(item, index, resultado_list):
        r = item['href']
        print(const_name + r)
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.get(const_name + r)
        pageSource = driver.page_source
        driver.quit()
        soup = BeautifulSoup(pageSource, 'html.parser')
        result = soup.find('div', {'id': 'reading-content'})
        title = soup.find('title').text
        resultado_list[index] = (item, result,title)
        
    # Número de threads que você deseja criar
    num_threads = 2

    # Criando uma lista compartilhada para armazenar os resultados
    resultado_list = [None] * len(card_inv)

    # Criando as threads
    threads = []
    for index, item in enumerate(card_inv):
        t = threading.Thread(target=processar_item, args=(item, index, resultado_list))
        threads.append(t)
        t.start()

    # Aguardando todas as threads terminarem
    for t in threads:
        t.join()

    # Imprimindo os resultados na ordem correta
    for item, result,title in resultado_list:
        c = pypub.create_chapter_from_string(result, title=title)
        my_first_epub.add_chapter(c)
    my_first_epub.create_epub(os.getcwd()+'/ebooks')
reaperscans()
