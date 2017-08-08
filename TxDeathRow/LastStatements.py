from bs4 import BeautifulSoup
from urllib.request import urlopen
import sqlite3


def getLastStatementText(lastStatementUrl):
    # Some offenders have no statement which all use the same URL
    if lastStatementUrl == 'https://www.tdcj.state.tx.us/death_row/dr_info/no_last_statement.html':
        return ''

    # Parse last statement HTML page for <p> tags
    LastStatementFile = urlopen(lastStatementUrl)
    LastStatementHtml = LastStatementFile.read()
    LastStatementFile.close()
    soup = BeautifulSoup(LastStatementHtml, "html.parser")
    paragraphs = soup.find_all('p')

    # Find the index of 'Last Statement:' and slice the array to
    # include only the paragraph tags after
    lastStatementIndex = 0
    for index, paragraph in enumerate(paragraphs):
        if paragraph.get_text().strip() == 'Last Statement:':
            lastStatementIndex = index
            break
    paragraphs = paragraphs[lastStatementIndex + 1:]

    # Clean up paragraphs
    lastStatementText = ''
    for paragraph in paragraphs:
        lastStatementText += paragraph.get_text()

    return lastStatementText


conn = sqlite3.connect('ExecutedOffenders.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS LastStatements
    (ExecutionId INTEGER PRIMARY KEY, LastStatement TEXT)''')
conn.commit()

lastStatementRows = []
cur.execute('''SELECT Execution, LastStatementLink FROM Offenders''')
#count = 0
for row in cur:
    print(row)
    lastStatementText = getLastStatementText(row[1])
    print(lastStatementText)
    lastStatementRows.append((row[0], lastStatementText))
    # Used for testing to pull just 3 records to limit site hits.
    #count += 1
    # if count > 2:
    #    break

cur.executemany("""INSERT OR IGNORE INTO
    LastStatements (ExecutionId, LastStatement)
    VALUES (?,?)""", lastStatementRows)
conn.commit()
cur.close()
conn.close()
