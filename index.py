import os
import sqlite3
import win32api

conn = sqlite3.connect('file_index.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS files
             (name text, path text)''')
conn.commit()

drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]

for drive in drives:
    for root, dirs, files in os.walk(drive):
        for name in files:
            path = os.path.join(root, name)
            c.execute("INSERT INTO files (name, path) VALUES (?, ?)", (name, path))
            print(name)
    conn.commit()
conn.close()
