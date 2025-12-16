import sqlite3

DB_NAME = "queue.db"

def get_conn():
    conn = sqlite3.connect(DB_NAME, timeout=30, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn

def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT NOT NULL CHECK(status IN ('pending','in_progress','done')),
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            started_at TEXT,
            finished_at TEXT,
            consumer_id TEXT
        );
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status_id ON tasks(status, id);")
    conn.close()

if __name__ == "__main__":
    init_db()
    print("DB initialized:", DB_NAME)