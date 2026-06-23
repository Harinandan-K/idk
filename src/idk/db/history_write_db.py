import logging
from pathlib import Path
from idk.db import create_db


logger = logging.getLogger(__name__)
logger.info('INFO_LOGGING_OPERATIONS')

CLEAN_HISTORY_FILE: Path = Path(__file__).resolve().parent.parent / 'etc' / 'clean_shell_history.txt'


def read_clean_history(clean_file: Path = CLEAN_HISTORY_FILE) -> list[str]:
    if  not clean_file.exists():
        logger.error(f'ERR_CLEAN_HISTORY_FILE_NOT_FOUND -> {clean_file}')
        return []

    with open(clean_file, 'r', encoding='utf-8', errors='ignore') as f:
        cmd_list: list[str] = [line.strip() for line in f if line.strip()]

    logger.info(f'OK_CLEAN_HISTORY_READ -> {len(cmd_list)} commands found')
    return cmd_list


def push_to_db(cmd_list: list[str]) -> str:
    if  not cmd_list:
        logger.warning('WARN_NO_COMMANDS_TO_PUSH')
        return ('WARN_NO_COMMANDS_TO_PUSH')

    try:
        with create_db.get_connection() as conn:
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
    cmd_list = read_clean_history()
    if not cmd_list:
        return ('ERR_CLEAN_HISTORY_FILE_NOT_FOUND')
    return push_to_db(cmd_list)


if __name__ == '__main__':
    print(ingest_clean_history())