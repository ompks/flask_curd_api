import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

query = "CREATE TABLE USERS (ID INTEGER PRIMARY KEY, USERNAME TEXT, PASSWORD TEXT)"

connection.execute(query)
connection.commit()
connection.close()