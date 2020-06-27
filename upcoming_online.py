from artworks_getter import *
from img_to_s3 import *


r = get_all_artworks_all_auctions(browser, 'online_auctions.txt', 'online_null_counter.txt', 'Online', 1)

browser.close()

print(r[0])
print(r[1])
print(r[2])

with open('online_artworks.txt', 'w') as file:
    json.dump(processed, file)

pictures = r[1]

for image in pictures:
    sale_id = image[0]
    lot_number = image[1]
    img_url = image[2]

    name = sale_id + '_' + str(lot_number)

    download_img(img_url)

    upload_to_s3('img.jpg', 'mytestbucket2020june', 'Christies_images', name)


