import json
import numpy as np
from bs4 import BeautifulSoup
import time
import requests

def get_auctions(name_online, name_offline):
    # Here name_online is 'online_auctions.txt'.
    with open(name_online) as file:
        auctions_online = json.load(file)

    # Here name_offline is 'offline_auctions.txt'
    with open(name_offline) as file:
        auctions_offline = json.load(file)

    url = 'https://www.christies.com/Calendar'

    r = requests.get(url)

    time.sleep(3)

    soup = BeautifulSoup(r.text, 'html.parser')

    links = soup.find_all('a')

    results_online = []
    results_offline = []

    for link in links:
        l = link.get('href')
        if l!= None and l.find('SaleID') > -1:
            if l.find('onlineonly') > -1:
               results_online.append(l)
            else:
               results_offline.append(l)

    results_online = np.array(results_online)
    results_online = np.unique(results_online)

    results_offline = np.array(results_offline)
    results_offline = np.unique(results_offline)

    print(results_online)
    print(results_offline)

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

get_auctions('online_auctions.txt', 'offline_auctions.txt')



