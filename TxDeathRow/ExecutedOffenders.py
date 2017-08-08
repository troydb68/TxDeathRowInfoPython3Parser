from bs4 import BeautifulSoup
from urllib.request import urlopen
import sqlite3

conn = sqlite3.connect('ExecutedOffenders.sqlite')
cur = conn.cursor()

# Create Offenders Table if it does not already exist
cur.execute('''CREATE TABLE IF NOT EXISTS Offenders
    (Execution INTEGER PRIMARY KEY, InfoLink TEXT, LastStatementLink TEXT,
     LastName TEXT, FirstName TEXT, TDCJ_Number INTEGER, Age INTEGER,
     BirthDate DATE, Race TEXT, County TEXT)''')
conn.commit()

# Open Texas Death Row Execution Web site and read in all HTML
deathrowFile = urlopen("https://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html")
deathrowHtml = deathrowFile.read()
deathrowFile.close()

soup = BeautifulSoup(deathrowHtml, "html.parser")
deathrowTableCol = soup.table
offender = []
offenders = []
rowCount = 0

# Using BeautifulSoup4 extract all the table data
for row in deathrowTableCol.find_all('td'):
    if rowCount > 0 and rowCount % 10 == 0:
        offenders.append(offender)
        offender = []

# For the columns that contain hyperlinks add the domain to the link
    if len(row.find_all('a')) == 1:
        rowTitle = row.a['href']
        offender.append("https://www.tdcj.state.tx.us/death_row/" + rowTitle)
    else:
        offender.append(row.get_text())

    rowCount += 1

# Put all of the death row inmate info in to the Offenders table
cur.executemany("""INSERT OR IGNORE INTO
    Offenders (Execution, InfoLink, LastStatementLink, LastName, FirstName,
    TDCJ_Number, Age, BirthDate, Race, County)
    VALUES (?,?,?,?,?,?,?,?,?,?)""", offenders)
conn.commit()
conn.close()
