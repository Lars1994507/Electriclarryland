import os
import sqlite3

fdir = os.path.dirname(__file__)

def getPath(fname):
    return os.path.join(fdir, fname)

sqliteDbPath = getPath("muesumDATA.sqlite")
setupSqlPath = getPath("createTable.sql")

if os.path.exists(sqliteDbPath):
    os.remove(sqliteDbPath)

sqliteCon = sqlite3.connect(sqliteDbPath)
sqliteCursor = sqliteCon.cursor()

with open(setupSqlPath) as setupSqlFile:
    setupSqlScript = setupSqlFile.read()

sqliteCursor.executescript(setupSqlScript)
sqliteCon.commit()

sqliteCursor.close()
sqliteCon.close()
print("Blank tables created successfully!")
