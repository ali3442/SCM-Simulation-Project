#import os
#if os.path.exists('products.db'):
#    os.remove('products.db') 
import sqlite3
from datetime import datetime

conn = sqlite3.connect('products.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        product_name TEXT NOT NULL,
        expiration_date TEXT NOT NULL
    )
''')
conn.commit() 

# Fixed product_exists function
def product_exists(product_id):
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM products WHERE product_id = ?", (product_id,))
    return cursor.fetchone() is not None

# Modified insert_product function
def insert_product(product_id: str, name: str, expiration_date: str):
    try:
        cursor.execute(
            "INSERT INTO products (product_id, product_name, expiration_date) "
            "VALUES (?, ?, ?)",
            (str(product_id), str(name), str(expiration_date))
        )
        conn.commit()
    except Exception as e:
        print(f"[DB ERROR] Failed to insert: {e}")
        conn.rollback()

def fetch_all_products():
    cursor.execute('SELECT * FROM products')
    return cursor.fetchall()

def close_product_connection():
    conn.close()