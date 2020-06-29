import json
import numpy as np
from bs4 import BeautifulSoup
import time
import requests

def get_auctions(file_name):
    with open(name_online) as file:
        auctions = json.load(file)

    url = 'https://www.christies.com/Results'

    r = requests.get(url)

    time.sleep(3)

    soup = BeautifulSoup(r.text, 'html.parser')

    links = soup.find_all('a')

    results = []

    for link in links:
        l = link.get('href')
        if l!= None and l.find('aspx?lid=1') > -1:
            results.append(l)

    results = results[3:]

    results = np.array(results)
    results = np.unique(results)

    for l in results:
        if l not in auctions:
            auctions[l] = False

    with open(file_name, 'w') as file:
        json.dump(auctions, file)
       

current_time = datetime.datetime.now()
current_time = current_time.strftime("%m"+"%d"+"%Y")

monitor = []

try:
    get_auctions('past_auctions.txt')
    monitor[current_time] = True
except:
    monitor[current_time] = False
    
auc_monitor_db(monitor, 'Past')

