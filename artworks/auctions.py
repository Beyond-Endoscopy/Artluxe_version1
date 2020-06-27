from bs4 import BeautifulSoup

class auction:
    def __init__(self, driver, url, time_of_auc = 'upcoming', location = 'Online'):
        self.url = url
        self.driver = driver
        self.artworks = []
        self.time_of_auc = time_of_auc
        self.location = location


    def get_artworks(self):
        url = self.url

        self.driver.get(url)

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        links = soup.find_all('a')

        if self.time_of_auc == 'upcoming':
            if self.location == 'Online':
                prefix = 'https://onlineonly.christies.com'
                for link in links:
                    l = link.get('href')
                    if l != None and l.find('/s/') > -1 and l.find('lang=') == -1:
                        l = prefix + l
                        self.artworks.append(l)
            else:
                for link in links:
                    l = link.get('href')
                    if l != None and l.find('lotfinder') > -1 and l.find('objectid') > -1:
                        self.artworks.append(l)

        else:
            self.location = soup.find('span', class_="col-xs-12 col-md-2 nopadl pad-right-20-auto-width").text


            if self.location == 'Online':
                prefix = 'https://onlineonly.christies.com'
                for link in links:
                    l = link.get('href')
                    if l != None and l.find('/s/') > -1 and l.find('lang=') == -1:
                        l = prefix + l
                        self.artworks.append(l)
            else:
                for link in links:
                    l = link.get('href')
                    if l != None and l.find('lotfinder') > -1 and l.find('intobjectid') > -1:
                        self.artworks.append(l)

        print (self.artworks)





