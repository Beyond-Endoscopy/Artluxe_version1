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
import pickle
from my_pycharm_functions import *
from my_pycharm_functions_2 import *


#Get the online auctions links.

online_links = []

for link in links:
    if link.find('onlineonly') > -1 and links[link] == False:
        online_links.append(link)

#Need to check the nonemptyness of online_links.
test = online_links[:2]

print(test)

#Open the virtual browser.

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(chrome_options=chrome_options)

#Get the artworks information.

r = get_all_artworks_all_auctions_online(browser, test)

print(links)

print(r)

browser.close()

processed = preprocess(r)

print(processed)
print(processed[0])

with open('auction_links.txt', 'w') as outfile:
    json.dump(links, outfile)

with open('artworks.txt', 'w') as file:
    json.dump(processed, file)


