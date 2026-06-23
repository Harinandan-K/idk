import logging
from pathlib import Path

from idk.db.database import get_connection

logger = logging.getLogger(__name__)
logger.info('INFO_LOGGING_OPERATIONS')

CLEAN_HISTORY_FILE: Path = Path(__file__).resolve().parent.parent / 'etc' / 'clean_shell_history.txt'


def read_clean_history(clean_file: Path = CLEAN_HISTORY_FILE) -> list[str]:
    """reads the cleaned command list produced by history_cleaner.py"""
    if not clean_file.exists():
        logger.error(f'ERR_CLEAN_HISTORY_FILE_NOT_FOUND -> {clean_file}')
        return []

    with open(clean_file, 'r', encoding='utf-8', errors='ignore') as f:
        # strip blank lines and trailing newlines, keep command text as-is
        cmd_list: list[str] = [line.strip() for line in f if line.strip()]

    logger.info(f'OK_CLEAN_HISTORY_READ -> {len(cmd_list)} commands found')
    return cmd_list


def push_to_db(cmd_list: list[str]) -> str:
    """
    pushes cleaned commands into the db.
    - commands table: catalog entry, one row per unique command (INSERT OR IGNORE
      so re-running this never errors on duplicates already present from a past run)
    - usage_logs table: one row per occurrence, this is what powers the adaptive
      sort / leaderboard feature later in analytics.py
    """
    if not cmd_list:
        logger.warning('WARN_NO_COMMANDS_TO_PUSH')
        return ('WARN_NO_COMMANDS_TO_PUSH')

    try:
        with get_connection() as conn:
            # description is NOT NULL in the schema, empty string is a safe
            # placeholder until the whatis fallback backfills real descriptions
            conn.executemany(
                "INSERT OR IGNORE INTO commands (name, description) VALUES (?, ?)",
                [(cmd, '') for cmd in cmd_list]
            )

            conn.executemany(
                "INSERT INTO usage_logs (command_name) VALUES (?)",
                [(cmd,) for cmd in cmd_list]
            )

        logger.info(f'OK_COMMANDS_PUSHED_TO_DB -> {len(cmd_list)} rows processed')
        return ('OK_COMMANDS_PUSHED_TO_DB')

    except Exception as err:
        logger.critical(f'FATAL_DB_PUSH_FAILED -> {err}')
        return ('FATAL_DB_PUSH_FAILED')


def ingest_clean_history() -> str:
    """entrypoint: read clean_shell_history.txt and push every command into the db"""
    cmd_list = read_clean_history()
    if not cmd_list:
        return ('ERR_CLEAN_HISTORY_FILE_NOT_FOUND')
    return push_to_db(cmd_list)


if __name__ == '__main__':
    print(ingest_clean_history())