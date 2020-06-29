import json
import psycopg2

sql = "UPDATE artworks_v2 SET price = %s, " \
      "time_updated = %s where sale_id = %s and lot_number = %s"

#password removed. 

def update_database(works):
    conn = psycopg2.connect(
        "dbname = 'postgres' user = 'postgrestest' host ='postgrestest.cfequksew9vz.us-east-1.rds.amazonaws.com' password='ZZZ'")

    cur = conn.cursor()

    print(works)

    l = len(works)

    for i in range(l):
        sale_id = works[i][0]
        lot_number = works[i][1]
        price = works[i][2]
        time_updated = works[i][3]

        val = (price, time_updated, sale_id, lot_number,)

        cur.execute(sql, val)

    conn.commit()

    conn.close()
