import requests
from bs4 import BeautifulSoup


import lxml.html
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pygsheets
import pandas as pd


def get_price(_which : str):
    target_url = "https://app.tabtrader.com/watchlist"
    driver = webdriver.Chrome("pathtochromedriver\chromedriver.exe")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-popup-blocking")

    driver.maximize_window()
    driver.get(target_url)

    time.sleep(3)

    wait = WebDriverWait(driver, 5)

    #button = driver.find_element(By.CLASS_NAME, "modal-button modal-button--save")
    buttons = driver.find_elements(By.CSS_SELECTOR, 'button')
    for l in buttons:
        if (l.text == 'Agree'):
            l.click()
            time.sleep(10)

    pSource= driver.page_source

    soup = BeautifulSoup(pSource, "html.parser")



    #print "The title of Article is : " + ArticleTitle.text
    Container = soup.find("div",{"title": _which })
    #Container = soup.find("div",{"title":"XBT/USD"})

    Parent = Container.find_parent()

    Texts=Parent.findAll("p")

    with open("result.txt", "w", encoding='utf-8') as file:
        #file.write(str(soup))
        for a in Texts:
            r = str(a.text)
            r = r.replace(chr(160), "")

            #for letter in r:
            # print(letter + " - " + str(ord(letter)))

            print(r)
            file.write(r)
            result = r

    print('Done')    
    return r



def write_in_excel(_cell : str, _price : str):
    #authorization
    gc = pygsheets.authorize(service_file='сюда путь к Json файлу с апи гугла')

    # Create empty dataframe
    df = pd.DataFrame()

    # Create a column
    df['name'] = ['John', 'Steve', 'Sarah']

    #open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
    sh = gc.open('сюда название экселя')

    #select the first sheet 
    wks = sh[0]

    #update the first sheet with df, starting at cell B2. 
    cell = wks.cell(_cell)
    cell.value = _price

    print('Written')


if __name__ == "__main__":
    # Какая карточка с сайта нужна (на примере "XBT/USD" )
    price = get_price("XBT/USD")
    # В какую ячейку забивать
    write_in_excel('A4', price)