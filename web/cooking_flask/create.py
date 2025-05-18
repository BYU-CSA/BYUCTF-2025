import sqlite3

# Connect to (or create) the SQLite database
conn = sqlite3.connect("cooking.sqlite")
cursor = conn.cursor()

# Read the SQL file
with open("creation_script.sql", "r") as f:
    sql_script = f.read()

# Execute SQL script
cursor.executescript(sql_script)

# Commit and close
conn.commit()
conn.close()

print("Database created and populated successfully.")
