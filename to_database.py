import json
import psycopg2

conn = psycopg2.connect("dbname = 'postgres' user = 'postgrestest' host ='postgrestest.cfequksew9vz.us-east-1.rds.amazonaws.com' password='66155376Ab'")

cur = conn.cursor()

sql = "INSERT INTO artworks (title, sale_id, lot_number, sale_date, " \
      "location, artist, auction_house, auction_title, estimate_text, " \
      "estimate_min, estimate_max, price, image_url, year, description, signed, size) VALUES " \
      "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

with open('artworks.txt', 'r') as file:
    works = json.load(file)

print(works)

l = len(works)

for i in range(l):
    title = works[i][0]
    sale_id = works[i][1]
    lot_number = works[i][2]
    sale_date = works[i][3]
    location = works[i][4]
    artist = works[i][5]
    auction_house = works[i][6]
    auction_title = works[i][7]
    estimate_text = works[i][8]
    estimate_min = works[i][9]
    estimate_max = works[i][10]
    price = works[i][11]
    image_url = works[i][12]
    year = works[i][13]
    description = works[i][14]
    signed = works[i][15]
    size = works[i][16]

    val = (title, sale_id, lot_number, sale_date, \
           location, artist, auction_house, auction_title, estimate_text, \
           estimate_min, estimate_max, price, image_url, year, description, signed, size,)

    cur.execute(sql, val)

conn.commit()

conn.close()
