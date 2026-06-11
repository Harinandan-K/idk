#Importing SQLite3 module
import sqlite3
DB_FILE= "commands.db"

#Establishing a connection with the database
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()


