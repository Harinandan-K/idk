import re
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logger.info('INFO_LOGGING_HISTORY_CLEANER')

class Cleaner():
    def __init__(self) -> None:
        self.loc_l0: int = 0
        self.dropped_count: int = 0
        self.loc_clean: int = 0


    def read_raw_data(self) -> list[str]:
        raw_shell_history: Path = Path(__file__).resolve().parent.parent / 'etc' / 'raw_shell_history_V0.txt'
        with open (raw_shell_history, 'r') as raw_file:
            history_list: list[str] = raw_file.readlines()
        logger.info("OK_RAW_DATA_READ")
        return history_list


    def meta_data_remove(self, history_list: list[str]) -> list[str]:
        METADATA = re.compile(r"^:\s*\d+:\d+;")
        meta_data_removed_list: list[str] = []
        for line in history_list :
            cleaned_line = re.sub(METADATA, "", line)
            meta_data_removed_list.append(cleaned_line)
            self.loc_l0 += 1
            logger.debug(f'DEBUG_LOC_RAW = {self.loc_l0}')
        logger.info("OK_META_DATA_STRIPPED_FROM_RAW_HISTORY")
        return meta_data_removed_list


    def duplicate_cmd_remove(self, meta_data_removed_list: list[str]) -> list[str]:
        duplicate_removed_list: list[str] = list(dict.fromkeys(meta_data_removed_list))
        logger.info("OK_DUPLICATE_CMD_REMOVED")
        return duplicate_removed_list
        

    def ignore_cmd_file_read(self) -> set[str]:
        ignore_file_path = Path(__file__).resolve().parent.parent / 'etc' / 'ignore_cmd_list.txt'
        if not ignore_file_path.exists():
            logger.error("ERR_IGNORE_CMD_FILE_NOT_FOUND")
            return set()    
        with open(ignore_file_path, 'r') as ignore_file:
            ignore_cmd_set: set[str] = set()
            for line in ignore_file:
                clean_line = line.strip()          
                if clean_line:
                    ignore_cmd_set.add(clean_line)
            logger.info('OK_IGNORE_CMD_FILE_FOUND_AND_READ')
            return ignore_cmd_set


    def common_cmd_remove(self, duplicate_removed_list: list[str], ignore_cmd_set: set[str]) -> list[str]:
        common_cmd_removed_list: list[str] = []
        for line in duplicate_removed_list:
            base_command = line.split()[0] if line.split() else ""
            if base_command not in ignore_cmd_set:
                common_cmd_removed_list.append(line)  
        return common_cmd_removed_list
        

    def aggressive_filer(self, common_cmd_remove_list: list[str]) -> list[str]:
        ENV_VAR_PATTERN = re.compile(r'\b[A-Z0-9_]*(KEY|TOKEN|SECRET|PASSWORD)\s*=')
        FLAG_PATTERN = re.compile(r'(-p\s+[\w\W]+|--password=|-k\s+[\w\W]+)')
        URL_CRED_PATTERN = re.compile(r'https?:\/\/[^:\s]+:[^@\s]+@')
        KEYWORD_PATTERN = re.compile(r'\b(password|passwd|secret|token|api_key|apikey|bearer)\b', re.IGNORECASE)
        THE_NUKE = [ENV_VAR_PATTERN, FLAG_PATTERN, URL_CRED_PATTERN, KEYWORD_PATTERN]
        sterile_list: list[str] = []
        self.dropped_count = 0
        for line in common_cmd_remove_list:
            is_pwd = False
            for pattern in THE_NUKE:
                if pattern.search(line): 
                    is_pwd = True
                    break 
            if not is_pwd:
                sterile_list.append(line)
            else:
                self.dropped_count += 1 
        return sterile_list


    def clean_file_write(self, cleaned_line_list: list[str]) -> None:
        clean_shell_history_file_path: Path = Path(__file__).resolve().parent.parent / 'etc' / 'clean_shell_history.txt'
        with open(clean_shell_history_file_path, "w") as raw:
            for line in cleaned_line_list:
                raw.write(line)
            logger.info(f'OK_CLEANED_HISTORY_WRITTEN -> {self.loc_clean} safe lines saved to {clean_shell_history_file_path}')


    def shred_raw_data(self) -> None:
        raw_shell_history: Path = Path(__file__).resolve().parent.parent / 'etc' / 'raw_shell_history.txt'
        if raw_shell_history.exists():
            raw_shell_history.unlink()
            logger.info("OK_RAW_DATA_SHREDDED -> The dirty raw shell history file has been completely vaporized.")


    def clean_cycle(self) -> None:
        logger.info("OK_CLEANING_CYCLE_STARTED")
        history = self.read_raw_data()
        meta_data_removed_list = self.meta_data_remove(history)
        duplicate_removed_list = self.duplicate_cmd_remove(meta_data_removed_list)
        ignore_cmd_set = self.ignore_cmd_file_read()
        common_cmd_remove_list = self.common_cmd_remove(duplicate_removed_list, ignore_cmd_set)
        aggressive_filter_list = self.aggressive_filer(common_cmd_remove_list)
        self.loc_clean = len(aggressive_filter_list)
        self.clean_file_write(aggressive_filter_list)
        self.shred_raw_data()
        
        logger.info(f"STATS -> Raw: {self.loc_l0} | Dropped: {self.dropped_count} | Final: {self.loc_clean}")


def history_cleaner() -> str:
    my_machine = Cleaner()
    my_machine.clean_cycle()
    return 'OK_ALL_CLEAN_CYCLE_SUCCESS'