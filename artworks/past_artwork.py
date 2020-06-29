from bs4 import BeautifulSoup
import datetime

class past_artwork:
    def __init__(self, driver, url, location):
        self.url = url
        self.driver = driver
        self.location = location
        self.info = []
        self.next_link = None

#The past artwork get_artwork_info function only collect sale_id, lot_number (these two together is the artwork id) and price.
#'xxx' is the website's name.

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

            # Get pricing
            # Here there is a problem, why it spits out None?
            try:
                price_text = soup.find('div', class_="price-realised row").text
                price = float(price_text[20:].replace(',', ""))
                currency = price_text[16:19]
            except:
                price = None
                currency = None

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

        else:
            next_link = soup.find('a', class_="icon xxx-icon_right-arrow button-icon icon_mask-text square")[
                'href']

            # Get Auction Info
            try:
                sale_id = soup.find('span', id="main_center_0_lnkSaleNumber").text.strip()
            except:
                sale_id = None

            # Get pricing
            try:
                price_text = soup.find('p', id="main_center_0_lblPriceRealizedPrimary").text
                price = float(price_text[4:].replace(',', ""))
                currency = price_text[:4]
            except:
                price = None
                currency = None

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

        timestamp = str(datetime.datetime.now())[:19]

        self.info.append(sale_id)
        self.info.append(lot_number)
        self.info.append(price)
        self.info.append(timestamp)

        self.next_link = next_link
