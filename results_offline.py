from past_artworks_getter import *

r = get_all_artworks_all_auctions(browser, 'past_auctions.txt', 'past_null_counter.txt', 'Offline', 1)

browser.close()

print(r[0])
print(r[1])