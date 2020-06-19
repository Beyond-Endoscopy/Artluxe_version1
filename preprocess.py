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

filename = 'MultinomialNBClassifier_v1.0.pkl'

with open(filename, 'rb') as file:
    mnb_model = pickle.load(file)

mnb = mnb_model['model']


def reverse_dic(dic):
    result = {}
    for key in dic:
        if dic[key] not in result:
            result[dic[key]] = key
        else:
            result[dic[key]] = result[dic[key]] + ', ' + key
    return result


def get_more_features(dic):
    tup = ()
    tup += (dic.get('medium'),)
    tup += (dic.get('year'),)
    tup += (dic.get('signature'),)
    tup += (dic.get('size'),)
    tup += (dic.get('other'),)
    return tup


def detail_to_tuple(lst):
    dic = mnb.predict(lst)
    dic = reverse_dic(dic)
    tup = get_more_features(dic)
    return tup


def more_features(info_1, info_2):
    info = []
    l = len(info_1)
    for i in range(l):
        tup = detail_to_tuple(info_2[i])
        info.append(info_1[i] + tup)
    return info


# Get a list of the auctions appear at the top of the webpage. We can adjust the url to get either the upcoming ones
# of the old ones.
def get_auctions(driver, url):
    driver.get(url)

    time.sleep(5)

    # The following line should be added on laptop.

    # driver.find_element_by_xpath("//button[normalize-space()='Accept Cookies']").click()

    # When getting upcoming auctions, we first click 'load more'.
    if url == 'https://www.christies.com/Calendar':
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

    results = []

    if url == 'https://www.christies.com/Results':
        for link in links:
            l = link.get('href')
            if l != None and l.find('aspx') > -1 and l.find('www') == -1:
                results.append(l)
    elif url == 'https://www.christies.com/Calendar':
        for link in links:
            l = link.get('href')
            if l != None and l.find('SaleID') > -1:
                results.append(l)

    results = np.array(results)
    results = np.unique(results)

    return results


def get_artworks(driver, url):
    driver.get(url)

    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Checking whether the auction happened online or not, since the links to the artworks have different formats.

    try:
        location = soup.find('span', class_="col-xs-12 col-md-2 nopadl pad-right-20-auto-width").text
    except:
        location = 'Not Online'

    links = soup.find_all('a')

    results = []

    if location == 'Online':
        prefix = 'https://onlineonly.christies.com'

        for link in links:
            l = link.get('href')
            if l != None and l.find('/s/') > -1 and l.find('lang=') == -1:
                l = prefix + l
                results.append(l)

        return results

    else:
        for link in links:
            l = link.get('href')
            if l != None and l.find('lotfinder') > -1 and l.find('objectid') > -1:
                results.append(l)

        return results