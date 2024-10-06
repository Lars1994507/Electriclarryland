import sqlite3

conn = sqlite3.connect('muesumDATA.sqlite')

cur = conn.cursor()

with open('createTable.sql', 'r') as sql_file:
    sql_script = sql_file.read()

cur.executescript(sql_script)

conn.commit()


