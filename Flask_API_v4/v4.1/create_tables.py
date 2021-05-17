import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

query_delete_users = 'DROP TABLE IF EXISTS users'
query_delete_store = 'DROP TABLE IF EXISTS store'
cursor.execute(query_delete_users)
cursor.execute(query_delete_store)

query_users = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)'
query_store = 'CREATE TABLE IF NOT EXISTS store (id INTEGER PRIMARY KEY, name text, price integer)'
cursor.execute(query_users)
cursor.execute(query_store)

connection.commit()
connection.close()
