import sqlite3
from datetime import datetime


con = sqlite3.connect('users.db')
c = con.cursor()


c.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        Email TEXT NOT NULL,
        pword TEXT NOT NULL
    )
''')

con.commit()


def insert_user( Email , pword ):
    
    c.execute('''
        INSERT INTO Users ( Email , pword )
        VALUES (?, ?)
    ''', ( Email , pword))
    con.commit()


def fetch_all_users():
    c.execute('SELECT * FROM Users')
    return c.fetchall()


def close_user_connection():
    con.close()
