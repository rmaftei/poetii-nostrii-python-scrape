from selenium import webdriver
from selenium.webdriver.common.by import By

from time import monotonic

start_time = monotonic()

WEBSITE = 'https://poetii-nostri.ro'
TITLE = 'Poetii nostri - Cele mai cunoscute poezii romanesti'
CSS_SELECTOR_POETI_CLASICI = 'body > div > div > div.main-container.col3-layout > div.main > div.col-wrapper > div.col-left.sidebar > div.block.block-cart > div > div > div > div > div > div > div > div > div > div.block-content > a'
CSS_SELECTOR_POETI_CONTEMPORANI = 'body > div > div > div.main-container.col3-layout > div.main > div.col-wrapper > div.col-left.sidebar > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div.block-content > a'
CSS_SELECTOR_POETI_STRAINI = 'body > div > div > div.main-container.col3-layout > div.main > div.col-wrapper > div.col-left.sidebar > div:nth-child(3) > div > div > div > div > div > div > div > div > div > div.block-content > a'

CSS_SELECTOR_PAGINA_POET_POEZII_LINK = 'body > div > div > div.main-container.col3-layout > div > div.col-wrapper > div.col-main > div > div > div > div > div > div > div > div > div > div.category-products > ul > li > div.product-col-1 > a'

CALE_FISIER = 'data'


NUMER_FISIER_SI_SELECTOR = [
    ("poeti_clasici.csv", CSS_SELECTOR_POETI_CLASICI),
    ("poeti_contemporani.csv", CSS_SELECTOR_POETI_CONTEMPORANI),
    ("poeti_straini.csv", CSS_SELECTOR_POETI_STRAINI)
    ]

def get_nume_si_link(css_selector):
    lista_poeti = browser.find_elements(By.CSS_SELECTOR, css_selector)

    nume_si_link = [(elem.text, elem.get_attribute('href')) for elem in lista_poeti]

    return nume_si_link

def get_poezie_si_link(nume, pagina):
    browser.get(pagina)

    lista_poezi = browser.find_elements(By.CSS_SELECTOR, CSS_SELECTOR_PAGINA_POET_POEZII_LINK)

    poezie_si_link = [(nume, pagina, elem.text, elem.get_attribute('href')) for elem in lista_poezi]

    return poezie_si_link
    
def scrie_in_fisier(nume_fisier):

    fisier = nume_fisier

    writer = open(f'{CALE_FISIER}/{fisier}', 'a')

    writer.write('nume,pagina poetului,titlul poeziei,pagina poeziei')

    def scrie(data_tuple):
        for (poet, pagina,titlu, link) in data_tuple:
            writer.write(f'\n"{poet}","{pagina}","{titlu}","{link}"') 

        return True
    
    return scrie


print("Start")

options = webdriver.FirefoxOptions()
options.add_argument('--headless')

browser = webdriver.Firefox(options=options)

browser.get(WEBSITE)

if browser.title != TITLE:
    print('Website it not loaded')
    browser.quit()
    quit()

poeti_si_pagina_lor = [(nume_fisier, get_nume_si_link(selector_css)) for (nume_fisier, selector_css) in NUMER_FISIER_SI_SELECTOR]

for nume_si_date in poeti_si_pagina_lor:

    nume_fisier = nume_si_date[0]
    poet_si_link_poezii = nume_si_date[1]

    print(f'Scriere {nume_fisier}')

    scrie_linie = scrie_in_fisier(nume_fisier)

    for poet, link in poet_si_link_poezii:

        lista_poezii = get_poezie_si_link(poet, link)
        
        scrie_linie(lista_poezii)
    
browser.quit()

print("Done")

print(f"Run time {monotonic() - start_time} seconds")
