import psycopg2 as db

conn_string = "dbname='nifi_db' host='postgres' user='root' password='root'"

conn=db.connect(conn_string)

cursor=conn.cursor()

query = "insert into users(id,name,street,city,zip) values ({}, '{}', '{}', '{}', '{}')".format(1, 'Big bird', 'Sesame Street', 'Fakeville', '12345')