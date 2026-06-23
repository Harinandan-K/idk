import os
import sys
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def os_check() -> str:
    compatable_os: list[str] = ['linux', 'darwin']
    if  sys.platform not in compatable_os:
        logger.critical('FATAL_OS_NOT_SUPPORTED')
        return('FATAL_OS_NOT_SUPPORTED')
    logger.info('OK_OS_SUPPORTED')
    return('OK_OS_SUPPORTED')


def shell_check() -> str:
    compatable_shell: list[str] = ['bash', 'zsh', 'fish']
    shell_dir: str | None = os.environ.get('SHELL')
    if  shell_dir != None:
        shell_dir_split: list[str] = shell_dir.split('/')
    else:
        logger.critical('FATAL_NO_SHELL_FOUND')
        return('FATAL_NO_SHELL_FOUND')
    
    global shell_name
    shell_name = shell_dir_split[-1]
    if  shell_name not in compatable_shell:
        logger.critical('FATAL_SHELL_NOT_SUPPORTED')
        return('FATAL_SHELL_NOT_SUPPORTED')
    logger.info('OK_SHELL_SUPPORTED')
    return('OK_SHELL_SUPPORTED')


def py_version_check() -> str:
    if sys.version_info <= (3, 10):
        logger.critical('FATAL_PY_VER_NOT_SUPPORTED')
        return('FATAL_PY_VER_NOT_SUPPORTED')
    logger.info('OK_PY_VER_SUPPORTED')
    return ('OK_PY_VER_SUPPORTED')


def file_perms_check() -> str:
    shell_history_path = Path.home() / f'.{shell_name}_history'

    try:
        with open(shell_history_path, "r"):
            logger.info(f'OK_SHELL_HISTORY_FILE_FOUND -> file found in {shell_history_path}')
            logger.info(f'OK_SHELL_HISTORY_FILE_READ_PERMS -> read access for the ./shell_history is granted')
            return('OK_SHELL_HISTORY_FILE_FOUND_WITH_READ_PERMS')
    except FileNotFoundError as warn:
        logger.warning(f'WARN_FILE_NOT_FOUND -> {warn}')
        return('WARN_FILE_NOT_FOUND')
    except PermissionError as err:
        logger.error(f'ERR_PERMISSION_DEINED -> {err}')
        return('ERR_PERMISSION_DEINED')
    

def base_checks() -> str :
    logger.info('INFO_LOGGING_BOOTSTRAP')

    os_check_return: str = os_check()
    if  os_check_return.startswith('FATAL_'):
        return (f'FATAL_BASE_CHECK_UNSUCCESSFULL -> {os_check_return} ')
    
    shell_check_return: str = shell_check()
    if  shell_check_return.startswith('FATAL_'):
        return (f'FATAL_BASE_CHECK_UNSUCCESSFULL -> {shell_check_return} ')
    
    py_check_return : str = py_version_check()
    if  py_check_return.startswith('FATAL'):
        return (f'FATAL_BASE_CHECK_UNSUCCESSFULL -> {py_check_return} ')
    
    file_perms_check_return: str = file_perms_check()
    if  file_perms_check_return.startswith('ERR_'):
        return (f'ERR_BASE_CHECK_ENCONUNTERED -> {file_perms_check_return} ')
    if file_perms_check_return.startswith('WARN_'):
        return (f'WARN_BASE_CHECK_ENCONUNTERED -> {file_perms_check_return} ')
    
    return ('MAIN_OK_ALL_BASE_CHECK_SUCCESS')


if  __name__ == '__main__':
    base_checks()
    print(os.environ.get('SHELL'))
