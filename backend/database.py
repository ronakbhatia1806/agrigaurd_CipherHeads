import sqlite3

DB_PATH = "security_logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record TEXT,
            hash_value TEXT
        )
    """)

    conn.commit()
    conn.close()

def store_hash_entry(record, hash_value):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO logs (record, hash_value) VALUES (?, ?)", (record, hash_value))
    conn.commit()
    conn.close()

# initialize at import
init_db()
