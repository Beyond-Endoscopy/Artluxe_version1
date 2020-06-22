import json
import pandas as pd
import numpy as np
import urllib3
from bs4 import BeautifulSoup
import re
import time
import datetime
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager





def get_histo_auctions(driver, name):
    with open(name) as file:
        auctions = json.load(file)

    url = 'https://www.christies.com/Results'
    driver.get(url)

    time.sleep(5)

    # The following line should be added on laptop.

    # driver.find_element_by_xpath("//button[normalize-space()='Accept Cookies']").click()

    # When getting upcoming auctions, we first click 'load more'.

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    links = soup.find_all('a')

    results = []


    for link in links:
        l = link.get('href')
        if l != None and l.find('aspx') > -1 and l.find('www') == -1:
            results.append(l)


    results = np.array(results)
    results = np.unique(results)

    prefix = 'https://www.christies.com'

    for l in results:
        l = prefix + l
        if l not in auctions:
            auctions[l] = False

    with open(name, 'w') as file:
        json.dump(auctions, file)




from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(chrome_options=chrome_options)

with open('histo_link_monitor.txt') as file:
    monitor = json.load(file)

current_time = datetime.datetime.now()
current_time = current_time.strftime("%m"+"%d"+"%Y")

try:
   get_histo_auctions(browser, 'histo_auctions.txt')
   monitor[current_time] = True
except:
    monitor[current_time] = False

with open('histo_link_monitor.txt', 'w') as file:
    json.dump(monitor, file)

browser.close()