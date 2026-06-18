import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logger.info('INFO_LOGGING_HISTORY_READER')


def shell_name_finder() -> str:
    shell_dir: str | None = os.environ.get('SHELL')
    if shell_dir is None:
        raise ValueError('No shell')
    logger.debug('DEBUG_FIX_NONE_SPLIT -> made a loop to rise error when shell none (all coz split is a puzzy)')
    shell_dir_split: list[str] = shell_dir.split('/')
    shell_name: str = shell_dir_split[-1]
    return(shell_name)


def shell_history_path_finder(shell_name: str) -> Path:
    shell_history_path = Path.home() / f'.{shell_name}_history'
    return(shell_history_path)


def history_reader(shell_history_path: Path)-> str:
    with open(shell_history_path, "r", encoding="utf-8", errors="ignore") as shell_history:
        logger.info('OK_FILE_READING_DONE')
        history: str = shell_history.read()
        return(history)
    
    
def history_store(history: str)-> None:
    raw_shell_history: Path = Path(__file__).resolve().parent.parent / 'etc' / 'raw_shell_history.txt'
    with open(raw_shell_history, "w") as raw:
        raw.write(history)
        logger.info(f'OK_RAW_HISTORY_WRITTEN -> all raw data written to {raw_shell_history}')


def history_read() -> str:
    shell_name = shell_name_finder()
    shell_history_path = shell_history_path_finder(shell_name)
    history = history_reader(shell_history_path)
    history_store(history)

    return('OK_RAW_HISTORY_UPDATED_TO_TEXT_FILE')