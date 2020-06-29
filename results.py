from artworks.past_artworks_getter import *
from to_database.update_db import *

#The same as the comment in 'upcoming_online.py', instead using 'past_auctions.txt' which stores the past auction links.

r = get_all_artworks_all_auctions(browser, 'past_auctions.txt', 1)

browser.close()

print(r[0])
print(r[1])

#update the database.
update_database(r[0])
