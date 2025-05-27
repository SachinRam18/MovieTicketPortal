import sqlite3

with open("setup.sql") as f:
    setup_script = f.read()

conn = sqlite3.connect("database.db")
conn.executescript(setup_script)
conn.commit()
conn.close()

print("✅ Database initialized successfully.")
