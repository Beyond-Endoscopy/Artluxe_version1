from artworks.artworks_getter import *
from to_database.insert_to_db import *
from to_database.monitor_to_db import *

r = get_all_artworks_all_auctions(browser, 'offline_auctions.txt', 'Offline', 1)

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

    upload_to_s3('img.jpg', 'my bucket name', 'xxx_images', name)

artworks_to_database(r[0])
null_counter_db(r[2])
