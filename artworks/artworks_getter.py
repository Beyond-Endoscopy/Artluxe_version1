import json
from artwork import *
from auctions import *

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(chrome_options=chrome_options)

#This function collect all the artworks in the auction of the link 'auc_link'.

def get_all_artworks(driver, auc_link, loc):
    auc = auction(driver, auc_link, location = loc)
    auc.get_artworks()
    link = auc.artworks[0]

    result = []
    image_urls = []
    count = 0
    null_count = 0

    while link != None:
        try:
            work = artwork(driver, link, location=loc)
            work.get_artwork_info()
            time.sleep(3)
            work.get_extended_info()
            info = work.extended_info
            print(info)
            result.append(info)
            image_urls.append(work.image)
            if work.info.count(None) == len(work.info):
                null_count += 1
            count += 1
            link = work.next_link
        except:
            break


    return result, image_urls, count, null_count

#This function collect all the artworks from all the auctions stored in the txt file 'auction_links_name' provided the information was not collected before.
#'number_of_auctions' controls the number of auctions from which we want to collect the information. We collect all if not specified.

def get_all_artworks_all_auctions(driver, auction_links_name, location, number_of_auctions = None):
    # Here auction_links_name is 'online_auctions.txt'.
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

    print(list_auctions)

    null_counter = {}

    result = []

    image_links = []

    n = len(list_auctions)
    for i in range(n):
        try:
           r = get_all_artworks(driver, list_auctions[i], loc=location)
           print(r[0])
           result = result + r[0]
           image_links = image_links + r[1]
           if list_auctions[i] not in null_counter:
                null_counter[list_auctions[i]] = [r[2], r[3]]
           auction_links[list_auctions[i]] = True
        except:
           pass

    with open(auction_links_name, 'w') as file:
        json.dump(auction_links, file)

    return result, image_links, null_counter

