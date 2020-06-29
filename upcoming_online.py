from artworks.artworks_getter import *
from to_database.img_to_s3 import *
from to_database.insert_into_db import *

#The txt file store the auction links. It is a dictionary with key the link and value True or False. 
#Once the information of a certain auction is collected, the value is updated from False to True. 1 is the number of auctions we want to 
#collect the artworks information, it can be other than 1.

r = get_all_artworks_all_auctions(browser, 'online_auctions.txt', 'Online', 1)

browser.close()

print(r[0])
print(r[1])
print(r[2])

pictures = r[1]

for image in pictures:
    sale_id = image[0]
    lot_number = image[1]
    img_url = image[2]

    name = sale_id + '_' + str(lot_number)

    download_img(img_url)

#xxx is the name of the website. There is a folder named 'xxx_images' in my S3 bucket.

    upload_to_s3('img.jpg', 'mytestbucket2020june', 'xxx_images', name)

#Write the information into the database.
artworks_to_database(r[0])


