import sqlite3
import pandas as pd


def get_db():
    conn = sqlite3.connect('CluedoMaster.db')
    return conn


def locations():
    db = get_db()
    result = pd.read_sql('SELECT * FROM Location', db)['Name']
    db.close()
    return result


def suspects():
    db = get_db()
    result = pd.read_sql('SELECT * FROM Suspect', db)['Name']
    db.close()
    return result


def weapons():
    db = get_db()
    result = pd.read_sql('SELECT * FROM Weapon', db)['Name']
    db.close()
    return result