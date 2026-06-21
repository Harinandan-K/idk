import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_FILE = Path(__file__).parent / "commands.db"

# context manager to handle connection, commit, rollback and closure
@contextmanager
def get_connection(path=DB_FILE):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    try:
        # WAL mode keeps reads fast and non-blocking during writes
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db(path=DB_FILE):
    with get_connection(path) as conn:
        conn.executescript("""
            -- stores commands and their descriptions
            -- name is the primary key, so duplicates are blocked at schema level
            CREATE TABLE IF NOT EXISTS commands (
                name        TEXT PRIMARY KEY,
                description TEXT NOT NULL
            );

            -- tracks every time a command is used
            -- cascades delete so logs clean up if a command is removed
            CREATE TABLE IF NOT EXISTS usage_logs (
                log_id       INTEGER PRIMARY KEY AUTOINCREMENT,
                command_name TEXT      NOT NULL,
                executed_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (command_name)
                    REFERENCES commands(name) ON DELETE CASCADE
            );

            -- b-tree index on command_name for fast leaderboard queries
            CREATE INDEX IF NOT EXISTS idx_logs_command_name
                ON usage_logs(command_name);
        """)

if __name__ == "__main__":
    init_db()
    print(f"[idk] database initialised at: {DB_FILE}")
