import numpy as np
from bs4 import BeautifulSoup
import datetime
import time
import requests
import pickle

#Due to copyrights, the model is not uploaded here.
filename = '~/Artluxe_version1/artworks/nlp_model/MultinomialNBClassifier_v1.0.pkl'

with open(filename, 'rb') as file:
    mnb_model = pickle.load(file)

mnb = mnb_model['model']

class artwork:
    def __init__(self, driver, url, location):
        self.url = url
        self.driver = driver
        self.location = location
        self.info = []
        self.extended_info = []
        self.image = []
        self.detail = []
        self.next_link = None

#'xxx' is the name of the website, I removed it due to my clients request.
    def get_artwork_info(self):
        url = self.url

        self.driver.get(url)

        time.sleep(3)

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        if self.location == 'Online':
            try:
                next_link = soup.find('span', class_="xxx-icon_right-arrow")['href']
                next_link = 'https://onlineonly.xxx.com' + next_link.split('href=')[1]
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

            auction_house = "xxx"
            auction_title = sale_of
            buyers_premium = True
            buyers_premium_perc = None

            # Get pricing
            # Here there is a problem, why it spits out None?
            try:
                price_text = soup.find('div', class_="price-realised row").text
                price = float(price_text[20:].replace(',', ""))
                currency = price_text[16:19]
            except:
                price = None
                currency = None

            # Get Estimate
            try:
                estimate_text = soup.find('div', class_="estimated row").text.lstrip().rstrip()
            except:
                estimate_text = None

            x = estimate_text.find('\n')

            if x > -1:
                est = estimate_text[:x]

                try:
                    estimate_min = float(est.split(' - ')[0][14:].replace(',', ""))
                    estimate_max = float(est.split(' - ')[1][4:].replace(',', ""))
                    if currency == None:
                        currency = est[10:13]
                except:
                    estimate_min = None
                    estimate_max = None

            else:
                try:
                    estimate_min = float(estimate_text.split(' - ')[0][14:].replace(',', ""))
                    estimate_max = float(estimate_text.split(' - ')[1][4:].replace(',', ""))
                    if currency == None:
                        currency = estimate_text[10:13]
                except:
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

        else:
            next_link = soup.find('a', class_="icon xxx-icon_right-arrow button-icon icon_mask-text square")[
                'href']

            sale_date = soup.find('p', id="main_center_0_lblSaleDate").text

            # Get Auction Info
            try:
                sale_id = soup.find('span', id="main_center_0_lnkSaleNumber").text.strip()
            except:
                sale_id = None

            try:
                sale_of = soup.find('div', id="main_center_0_lblSaleTitle").text
                location = soup.find('p', id="main_center_0_lblSaleLocation").text
            except:
                sale_of = None
                location = None

            auction_house = "xxx"
            auction_title = sale_of
            buyers_premium = True
            buyers_premium_perc = None

            # Get pricing
            try:
                price_text = soup.find('p', id="main_center_0_lblPriceRealizedPrimary").text
                price = float(price_text[4:].replace(',', ""))
                currency = price_text[:4]
            except:
                price = None
                currency = None

            # Gest Estimate
            try:
                estimate_text = soup.find('span', id="main_center_0_lblPriceEstimatedPrimary").text
                estimate_min = float(estimate_text.split(' - ')[0][4:].replace(',', ""))
                estimate_max = float(estimate_text.split(' - ')[1][4:].replace(',', ""))
                if currency == None:
                    currency = estimate_text[:4]
            except:
                estimate_min = None
                estimate_max = None

            # Get Lot Number
            try:
                lot_number = soup.find('span', id="main_center_0_lblLotNumber").text.strip()

                try:
                    lot_text = soup.find('span', id="main_center_0_lblPreLotHeaderText").text
                except:
                    lot_text = None

                try:
                    lot_number = int(lot_number)
                except:
                    pass

            except:
                lot_number = None
                lot_text = None

            #  Get Images

            try:
                image_url = soup.find('a', class_="panzoom--link")['href']
            except:
                image_url = None

            try:
                find_images = soup.findAll('img', class_="image")
                images = set(i['src'].strip('?w=400') for i in find_images)
                additional_images = [i for i in images]

            except:
                additional_images = None

            # Get Art Information

            try:

                artist = soup.find('span', id="main_center_0_lblLotPrimaryTitle").text
                title = soup.find('h2', id="main_center_0_lblLotSecondaryTitle", class_="itemName").text.strip()
            except:
                artist = None
                title = None

            # Get Object Information

            try:
                title_2 = soup.find('span', id="main_center_0_lblLotPrimaryTitle").text
                details_2 = soup.find('span', id='main_center_0_lblLotDescription').text
                details_2 = details_2.split('\n')

                try:
                    image_url = soup.find('a', class_="panzoom--link")['href']
                except:
                    image_url = None

                try:
                    maker = soup.find('h2', id="main_center_0_lblLotSecondaryTitle").text
                except:
                    maker = None
            except:
                title_2 = None
                details_2 = np.NaN

            # Get Provenance Information

            try:
                provenance = soup.find('p', id="main_center_0_lblLotProvenance").text
                provenance = provenance.split('\n')

            except:
                provenance = None

        timestamp = str(datetime.datetime.now())[:19]

        self.info.append(title)
        self.info.append(sale_id)
        self.info.append(lot_number)
        self.info.append(sale_date)
        self.info.append(location)
        self.info.append(artist)
        self.info.append(auction_house)
        self.info.append(auction_title)
        self.info.append(estimate_text)
        self.info.append(estimate_min)
        self.info.append(estimate_max)
        self.info.append(price)
        self.info.append(currency)
        self.info.append(timestamp)

        self.image.append(sale_id)
        self.image.append(lot_number)
        self.image.append(image_url)

        self.detail = details_2

        self.next_link = next_link

    def get_extended_info(self):
        self.extended_info = self.info

        classification = mnb.predict(self.detail)

        more_info = {}

        for key in classification:
            if classification[key] not in more_info:
                more_info[classification[key]] = key
            else:
                more_info[classification[key]] = more_info[classification[key]] + ',' + key

        self.extended_info.append(more_info.get('medium'))
        self.extended_info.append(more_info.get('year'))
        self.extended_info.append(more_info.get('signature'))
        self.extended_info.append(more_info.get('size'))
        self.extended_info.append(more_info.get('other'))










