import psycopg2



sql = "INSERT INTO artworks_v2 (title, sale_id, lot_number, sale_date, " \
      "location, artist, auction_house, auction_title, estimate_text, " \
      "estimate_min, estimate_max, price, currency, timestamp, medium, year, description, signed, size, time_updated) VALUES " \
      "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

def artworks_to_datbase(works):
    conn = psycopg2.connect(
        "dbname = 'postgres' user = 'postgrestest' host ='postgrestest.cfequksew9vz.us-east-1.rds.amazonaws.com' password='66155376Ab'")

    cur = conn.cursor()

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
        currency = works[i][12]
        timestamp = works[i][13]
        medium = works[i][14]
        year = works[i][15]
        description = works[i][16]
        signed = works[i][17]
        size = works[i][18]

        val = (title, sale_id, lot_number, sale_date, \
           location, artist, auction_house, auction_title, estimate_text, \
           estimate_min, estimate_max, price, currency, timestamp, medium, year, description, signed, size, None,)

        cur.execute(sql, val)

    conn.commit()

    conn.close()


