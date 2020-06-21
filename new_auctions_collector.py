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

def get_auctions(driver, name_online, name_offline):

#Here name_online is 'online_auctions.txt'.
    with open(name_online) as file:
        auctions_online = json.load(file)

#Here name_offline is 'offline_auctions.txt'
    with open(name_offline) as file:
        auctions_offline = json.load(file)

    url = 'https://www.christies.com/Calendar'
    driver.get(url)

    time.sleep(5)

    # The following line should be added on laptop.

    # driver.find_element_by_xpath("//button[normalize-space()='Accept Cookies']").click()

    # When getting upcoming auctions, we first click 'load more'.

    control = True
    while control:
        try:
            c = browser.find_element_by_xpath("//button[normalize-space()='Load more']")
            browser.execute_script("arguments[0].click();", c)

                # On local computer it is the following code,
                # browser.find_element_by_xpath("//button[normalize-space()='Load more']").click()

            time.sleep(5)
        except:
            control = False

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    links = soup.find_all('a')

    results_online = []
    results_offline = []



    for link in links:
        l = link.get('href')
        if l != None and l.find('SaleID') and l.find('onlineonly') > -1:
            results_online.append(l)
        if l != None and l.find('SaleID') and l.find('onlineonly') == -1:
            results_offline.append(l)

    results_online = np.array(results_online)
    results_offline = np.unique(results_offline)

    for l in results_online:
        if l not in auctions_online:
            auctions_online[l] = False

    for l in results_offline:
        if l not in auctions_offline:
            auctions_offline[l] = False

    print(auctions_online)
    print(auctions_offline)

    with open(name_online, 'w') as file:
        json.dump(auctions_online, file)

    with open(name_offline, 'w') as file:
        json.dump(auctions_offline, file)

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(chrome_options=chrome_options)

with open('new_link_monitor.txt') as file:
    monitor = json.load(file)

current_time = datetime.datetime.now()
current_time = current_time.strftime("%m"+"%d"+"%Y")

try:
    get_auctions(browser, 'online_auctions.txt', 'offline_auctions.txt')
    monitor[current_time] = True
except:
    monitor[current_time] = False


with open('new_link_monitor.txt', 'w') as file:
    json.dump(monitor, file)

browser.close()