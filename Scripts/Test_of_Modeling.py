import sqlite3

# Test of Modeling: Verify database creation and table structure

conn = sqlite3.connect("Data/data_cleaned.db")
cursor = conn.cursor()


# Check if tables were created successfully

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

print(cursor.fetchall())

conn.close()