import os
import sqlite3

fdir = os.path.dirname(__file__)

def getPath(fname):
    return os.path.join(fdir, fname)

sqliteDbPath = getPath("muesumDATA.sqlite")
setupSqlDataPath = getPath("populateTable.sql")

sqliteCon = sqlite3.connect(sqliteDbPath)
sqliteCursor = sqliteCon.cursor()

with open(setupSqlDataPath) as setupSqlDataFile:
    setupSqlDataScript = setupSqlDataFile.read()

sqliteCursor.executescript(setupSqlDataScript)
sqliteCon.commit()

sqliteCursor.close()
sqliteCon.close()
print("Tables populated successfully!")
