import sqlite3

conn = sqlite3.connect('muesumDATA.sqlite')

cur = conn.cursor()

with open('populateTable.sql', 'r') as sql_file:
    sql_script = sql_file.read()

cur.executescript(sql_script)

conn.commit()


