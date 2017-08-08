# TxDeathRowInfoPython3Parser
Python 3 Scripts to extract the Texas Death Row Inmate Information into Sqlite3 for further Data Analysis

https://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html

Capstone Project for Coursera Python3 Course:

ExecutedOffenders.py will create the Offenders table in ExecutedOffenders.sqlite database

LastStatements.py pulls the last statement of each offender.   If no Last Statement then NULL or None if that was input in to the table.

Note: BeautifulSoup4 is used for the parsing and would need to be installed on Python3 if not already using PIP.

