import sqlite3

conn = sqlite3.connect("farmers.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS farmers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    location TEXT,
    crop TEXT,
    land REAL
)
""")

conn.commit()
conn.close()
