import psycopg2

def auc_monitor_db(monitor, type):
    conn = psycopg2.connect("dbname = 'postgres' user = 'postgrestest' "
                            "host ='postgrestest.cfequksew9vz.us-east-1.rds.amazonaws.com' "
                            "password='66155376Ab'")

    cur = conn.cursor()

    sql1 = "INSERT INTO monitor (type, date, result) VALUES (%s, %s, %s)"

    for date in monitor:
        if monitor[date] == True:
            result = 'True'
        else:
            result = 'False'
        val = (type, date, result,)
        cur.execute(sql1, val)

    conn.commit()

    conn.close()

def null_counter_db(counter):
    conn = psycopg2.connect("dbname = 'postgres' user = 'postgrestest' "
                            "host ='postgrestest.cfequksew9vz.us-east-1.rds.amazonaws.com' "
                            "password='66155376Ab'")

    sql2 = "INSERT INTO null_counter (auction_link, number_of_items, number_of_null) VALUES (%s, %s, %s)"

    cur = conn.cursor()

    for link in counter:
        number_of_items = counter[link][0]
        number_of_null = counter[link][1]
        val = (link, number_of_items, number_of_null,)
        cur.execute(sql2, val)

    conn.commit()

    conn.close()