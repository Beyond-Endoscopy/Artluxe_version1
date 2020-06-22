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
from offline_artwork_getter import *
from img_to_s3 import *


#Open the virtual browser.

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(chrome_options=chrome_options)

#Get the artworks information.

r = get_all_artworks_all_auctions_online(browser, 'online_auctions.txt', 'new_online_null_counter.txt', 1)

print(r)

s = get_all_artworks_all_auctions_offline(browser, 'offline_auctions.txt', 'new_offline_null_counter.txt', 1)

print(s)

browser.close()

processed = preprocess(r[0])

print(processed)
print(processed[0])



with open('online_artworks.txt', 'w') as file:
    json.dump(processed, file)

pictures = r[1]

for image in pictures:
    sale_id = image[0]
    lot_number = image[1]
    img_url = image[2]

    name = sale_id + '_' + str(lot_number)

    download_img(img_url)

    upload_to_s3('img.jpg', 'mytestbucket2020june', 'Christies_images', name)

processed_offline = preprocess(s[0])

with open('offline_artworks.txt', 'w') as file:
    json.dump(processed, file)

pictures = s[1]

for image in pictures:
    sale_id = image[0]
    lot_number = image[1]
    img_url = image[2]

    name = sale_id + '_' + str(lot_number)

    download_img(img_url)

    upload_to_s3('img.jpg', 'mytestbucket2020june', 'Christies_images', name)





