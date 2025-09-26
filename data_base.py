import os, sqlite3
from dotenv import load_dotenv
load_dotenv()

DB_PATH = os.getenv("DB_PATH", "./aurora.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_database():
    conn = get_conn()
    sql_dir = os.path.join(os.path.dirname(__file__), "sql")
    for fname in sorted(os.listdir(sql_dir)):
        if fname.endswith(".sql"):
            path = os.path.join(sql_dir, fname)
            with open(path, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
    conn.commit()
    conn.close()
