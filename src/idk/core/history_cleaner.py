import re
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logger.info('INFO_LOGGING_HISTORY_CLEANER')


def read_raw_data() -> list[str]:
    raw_shell_history: Path = Path(__file__).resolve().parent.parent / 'etc' / 'raw_shell_history_V0.txt'
    with open (raw_shell_history, 'r') as raw_file:
        history_list: list[str] = raw_file.readlines()
    logger.info("OK_RAW_DATA_READ")
    return(history_list)


def meta_data_remove(history_list: list[str]) -> list[str]:
    METADATA = re.compile(r"^:\s*\d+:\d+;")
    meta_data_removed_list: list[str] = []
    for line in history_list :
        cleaned_line = re.sub(METADATA, "", line)
        meta_data_removed_list.append(cleaned_line)
    logger.info("OK_META_DATA_STRIPED_FROM_RAW_HISTORY")
    return meta_data_removed_list


def duplicate_cmd_remove(meta_data_removed_list: list[str]) -> list[str]:
    duplicate_removed_list: list[str] = list(dict.fromkeys(meta_data_removed_list))
    logger.info("OK_DUPLICATE_CMD_REMOVED")
    return duplicate_removed_list
    

def ignore_cmd_file_read() -> set[str]:
    ignore_file_path = Path(__file__).resolve().parent.parent / 'etc' / 'ignore_cmd_list.txt'
    if  not ignore_file_path.exists():
        logger.error("ERR_IGNORE_CMD_FILE_NOT_FOUND")
        return set()    
    with open(ignore_file_path, 'r') as ignore_file:
        ignore_cmd_set: set[str] = set()
        for line in ignore_file:
            clean_line = line.strip()          
            if clean_line:
                ignore_cmd_set.add(clean_line)
        logger.info('OK_INGORE_CMD_FILE_FOUND_AND_READ')
        return ignore_cmd_set


def common_cmd_remove(duplicate_removed_list: list[str], ignore_cmd_set: set[str]) -> list[str]:
    common_cmd_removed_list: list[str] = []
    for line in duplicate_removed_list:
        base_command = line.split()[0] if  line.split() else ""
        if  base_command not in ignore_cmd_set:
            common_cmd_removed_list.append(line)  
    return common_cmd_removed_list
    

def clean_cycle(history: list[str]) -> list[str]:
    logger.info("OK_CLEANING_CYCLE_STARED")
    meta_data_removed_list: list[str] = meta_data_remove(history)
    duplicate_removed_list: list[str] = duplicate_cmd_remove(meta_data_removed_list)
    ignore_cmd_set: set[str] = ignore_cmd_file_read()
    common_cmd_remove_list: list[str] = common_cmd_remove(duplicate_removed_list, ignore_cmd_set)
    return common_cmd_remove_list
    

def clean_file_write(cleaned_line_list: list[str]) -> None:
    clean_shell_history_file_path: Path = Path(__file__).resolve().parent.parent / 'etc' / 'clean_shell_history.txt'
    with open(clean_shell_history_file_path, "w") as raw:
        for line in cleaned_line_list:
            raw.write(line)
        logger.info(f'OK_CLEANED_HISTORY_WRITTEN -> all raw data written to {clean_shell_history_file_path}')


def history_cleaner() -> str:
    history: list[str] = read_raw_data()
    cleaned_cmd_list: list[str] = clean_cycle(history)
    clean_file_write(cleaned_cmd_list)

    return('OK_ALL_CLEAN_CYCLE_SUCCESS')
