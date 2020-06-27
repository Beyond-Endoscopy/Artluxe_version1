from past_artworks_getter import *
from update_db import *

r = get_all_artworks_all_auctions(browser, 'past_auctions.txt', 'past_null_counter.txt', 1)

browser.close()

print(r[0])
print(r[1])

update_database(r[0])