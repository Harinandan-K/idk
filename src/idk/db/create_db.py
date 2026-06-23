import sqlite3
from contextlib import contextmanager
from pathlib import Path
import logging 

logger = logging.getLogger(__name__)
logger.info('INFO_LOGGING_DB_CREATE')

DB_FILE = Path(__file__).parent / "IDK_USER.db"

@contextmanager
def get_connection(path : Path = DB_FILE):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row  
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db(path : Path = DB_FILE):
    with get_connection(path) as conn:
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS COMMANDS (
                CMD        TEXT PRIMARY KEY,
                DESC TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS USAGE_LOGS (
                LOG_ID       INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT    NOT NULL,
                EXECUTED_AT  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (command_name)
                    REFERENCES commands(name) ON DELETE CASCADE
            );

            
            CREATE INDEX IF NOT EXISTS idx_logs_command_name
                ON usage_logs(command_name);
        ''')


if  __name__ == "__main__":
    init_db()
    print(f"[idk] database initialised at: {DB_FILE}")
