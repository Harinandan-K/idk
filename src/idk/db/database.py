#Importing SQLite3 module
import sqlite3
DB_FILE= "commands.db"

#Establishing a connection with the database
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

#Creating the database 
cur.execute("""
    CREATE TABLE IF NOT EXISTS commands(
        name PRIMARY KEY,
        description TEXT NOT NULL
    )
""")

#Committing the changes
conn.commit()

#Closing the connection
conn.close()
