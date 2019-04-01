import sqlite3
import pandas as pd

db = sqlite3.connect('CluedoMaster.db')
cur = db.cursor()

#Location
Location = pd.DataFrame({
        'Id': ['L1','L2','L3','L4','L5','L6','L7','L8','L9'],
        'Name': ['Ballroom','Billiard Room','Conservatory','Dining Room','Hall','Kitchen','Library','Lounge','Study']})

#Suspect
Suspect = pd.DataFrame({
        'Id': ['S1','S2','S3','S4','S5','S6'],
        'Name': ['Green','Mustard','Peacock','Plum','Scarlet','White']})

#Weapon
Weapon = pd.DataFrame({
        'Id': ['W1','W2','W3','W4','W5','W6'],
        'Name': ['Candlestick','Knife','Lead Pipe','Revolver','Rope','Wrench']})

#Game


#Player


#Turn

#Write Data to SQLite Database
Location.to_sql(name='Location', con=db, if_exists='replace', index=True)
Suspect.to_sql(name='Suspect', con=db, if_exists='replace', index=True)
Weapon.to_sql(name='Weapon', con=db, if_exists='replace', index=True)
'''
#Import Capsule CSV File
df = pd.read_csv('SalesDialog.csv',delimiter=',')

#Delete unnecessary columns
df = df.drop('Opportunity Description',1)
df = df.drop('Email',1)
df = df.drop('Phone',1)
df = df.drop('Address',1)

#Rename columns
df = df.rename(columns={'Closed Date': 'Actual Close Date'
                        , 'Expected Closed Date': 'Expected Close Date'
                        , 'buyer cycle': 'Buyer cycle stage'})

#Set correct DataTypes
df['ReportDate'] = pd.to_datetime(df['ReportDate'], dayfirst = True).dt.date
df['Created'] = pd.to_datetime(df['Created'], dayfirst = True).dt.date
df['Updated'] = pd.to_datetime(df['Updated'], dayfirst = True).dt.date
df['Actual Close Date'] = pd.to_datetime(df['Actual Close Date'], dayfirst = True).dt.date
df['Expected Close Date'] = pd.to_datetime(df['Expected Close Date'], dayfirst = True).dt.date
df['Startdatum'] = pd.to_datetime(df['Startdatum'], dayfirst = True).dt.date
df.Probability = df.Probability.str.replace('%','').astype(int)/100

#Write Data to SQLite Database
df.to_sql(name='Capsule', con=db, if_exists='replace', index=False)

#Set index on OpportunityId & ReportDate
cur.execute('CREATE INDEX "Id" ON Capsule ("Opportunity Id");')
cur.execute('CREATE INDEX "RpDate" ON Capsule (ReportDate);')
'''

db.commit()
db.close()
