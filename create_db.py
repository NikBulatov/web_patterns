import sqlite3


with sqlite3.connect("db.sqlite3") as conn:
    cur = conn.cursor()
    with open("create_db.sql", "r") as f:
        text = f.read()
    cur.executescript(text)
    cur.close()
