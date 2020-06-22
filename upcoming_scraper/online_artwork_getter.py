
import numpy as np
from bs4 import BeautifulSoup
import re
import time
import datetime
import random
from selenium import webdriver
from preprocess import *


# Get the link of an artique, we collect all the information.
def get_online_lot_items(driver, url):
    driver.get(url)

    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    try:
        next_link = soup.find('span', class_="christies-icon_right-arrow")['href']
        next_link = 'https://onlineonly.christies.com' + next_link.split('href=')[1]
    except:
        next_link = None

    sale_id = soup.find('div', class_="col-xs-12 nopadl nopadr body-copy-small").text.strip()

    sale_date = soup.find('span', class_="col-xs-12 col-md-9 nopad").text.strip()
    location = 'Online'

    # Get Auction Info
    try:
        sale_of = soup.find('div', class_="col-xs-12 nopadl nopadr title").text.lstrip().rstrip()

    except:
        sale_of = None

    auction_house = "Christie's"
    auction_title = sale_of
    buyers_premium = True
    buyers_premium_perc = None

    # Get pricing
    # Here there is a problem, why it spits out None?
    try:
        price_text = soup.find('div', class_="price-realised row").text
        price = float(price_text[20:].replace(',', ""))
        currency = price_text[:4]
    except:
        price = None
        currency = None

    # Gest Estimate
    try:
        estimate_text = soup.find('div', class_="estimated row").text.lstrip().rstrip()
        estimate_min = float(estimate_text.split(' - ')[0][14:].replace(',', ""))
        estimate_max = float(estimate_text.split(' - ')[1][4:].replace(',', ""))
        if currency == None:
            currency = estimate_text[:4]
    except:
        estimate_text = None
        estimate_min = None
        estimate_max = None

    # Get Lot Number
    try:
        lot_number = soup.find('div', class_="lot-number").span.text
        lot_number = int(lot_number[4:])

        try:
            lot_number = int(lot_number)
        except:
            pass

        try:
            lot_text = soup.find('span', class_="pre-lot-text").text.strip()
        except:
            lot_text = None

    except:
        lot_number = None
        lot_text = None

    #  Get Images

    try:
        image_url = soup.find('div', class_="zoomTarget")['href']
    except:
        image_url = None

    try:
        find_images = soup.findAll('img', class_="center-block")
        images = set(i['src'].split('?')[0] for i in find_images)
        additional_images = [i for i in images]

    except:
        additional_images = None

    # Get Art Information

    try:
        title = soup.find('div', class_="maker").text.lstrip().rstrip()
        artist = soup.find_all('div', class_="title")[1].text.lstrip().rstrip()
    except:
        artist = None
        title = None

    # Get Object Information

    try:
        title_2 = soup.find('div', class_="bid-panel").find('div', class_="title").text.strip()
        details_2 = str(soup.find('div', class_='lot-notes-row').find('p'))
        details_2 = details_2.replace('<p>', "").replace("</p>", "").split('<br/>')

        try:
            image_url = soup.find('div', class_="zoomTarget")['href']
        except:
            image_url = None

        try:
            maker = soup.find('div', class_="bid-panel").find('div', class_="maker").text.strip()
        except:
            maker = None
    except:
        title_2 = None
        details_2 = np.NaN
        maker = None

    # Get Provenance Information

    for x in soup.findAll('div', class_='lot-notes-row'):
        try:
            info = x.find('div', 'row-title')
            info_header = info.text
            try:
                info_detail = str(x.find('p')).replace("<p>", "").replace('</p>', "").split("<br/>")
            except:
                info_detail = None
            if info_header == "Provenance":
                provenance = info_detail
        except:
            provenance = None
            continue

        # Get Provenance Information

    for x in soup.findAll('div', class_='lot-notes-row'):
        try:
            info = x.find('div', 'row-title')
            info_header = info.text
            try:
                info_detail = str(x.find('p')).replace("<p>", "").replace('</p>', "").split("<br/>")
            except:
                info_detail = None
            if info_header == "Provenance":
                provenance = info_detail
        except:
            provenance = None
            continue

    timestamp = str(datetime.datetime.now())[:19]

    val = (
    title, sale_id, lot_number, sale_date, location, artist, auction_house, auction_title, estimate_text, estimate_min,
    estimate_max, price, image_url)

    img_val = (sale_id, lot_number, image_url)

    return val, next_link, details_2, provenance, img_val






# Starting with an artique, getting all the information of it and the artiques after it in the same auction.
def get_all_artworks_info_online(driver, url):
    link = url

    result = []
    details = []
    image_urls = []
    count = 0
    null_count = 0

    while link != None:

            info_and_next_link = get_online_lot_items(driver, link)
            time.sleep(5)

            print(info_and_next_link)

            print(info_and_next_link[0])
            result.append(info_and_next_link[0])
            details.append(info_and_next_link[2])
            image_urls.append(info_and_next_link[4])
            count += 1
            if info_and_next_link[0].count(None) == len(info_and_next_link[0]):
                null_count += 1

            link = info_and_next_link[1]
            print(link)



    print(link)

    return result, details, count, null_count, image_urls


def get_all_artworks_all_auctions_online(driver, auction_links_name,  null_counter_name, number_of_auctions = None):

    #Here auction_links_name is 'online_auctions.txt'.
    with open(auction_links_name) as file:
        auction_links = json.load(file)

    list_auctions = []
    for auction in auction_links:
        if auction_links[auction] == False:
            list_auctions.append(auction)

    if len(list_auctions) == 0:
        print("No new jobs")
        return

    if number_of_auctions != None and len(list_auctions) > number_of_auctions:
        list_auctions = list_auctions[:number_of_auctions]
    else:
        pass


    null_counter = {}

    result = []

    image_links = []

    n = len(list_auctions)
    for i in range(n):
        try:
            art_works = get_artworks(driver, list_auctions[i])
            info, detail, count, null_count, image_urls = get_all_artworks_info_online(driver, art_works[0])
            result.append([info, detail])
            image_links += image_urls
            if list_auctions[i] not in null_counter:
                null_counter[list_auctions[i]] = (count, null_count)
            auction_links[list_auctions[i]] = True
        except:
            pass
    # In our test the null_counter_link would be 'new_online_null_counter.txt'.
    with open(null_counter_name, 'w') as file:
        json.dump(null_counter, file)

    with open(auction_links_name, 'w') as file:
        json.dump(auction_links, file)

    return result, image_links





def preprocess(lst):
    result = []

    n = len(lst)
    for i in range(n):
        #The model is used here.
        info, detail = lst[i][0], lst[i][1]
        all_info = more_features(info, detail)
        result += all_info



    return result
