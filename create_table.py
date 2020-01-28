import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

user_table = "CREATE TABLE IF NOT EXISTS USERS (ID INTEGER PRIMARY KEY, USERNAME TEXT, PASSWORD TEXT)"
connection.execute(user_table)

items_table = "CREATE TABLE IF NOT EXISTS ITEMS (ID INTEGER PRIMARY KEY, NAME TEXT, PRICE REAL)"
connection.execute(items_table)

connection.commit()
connection.close()