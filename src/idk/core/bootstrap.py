import os
import sys
import logging

logger = logging.getLogger(__name__)


def os_check() -> str:
    compatable_os: list[str] = ["linux", "darwin"]
    if  sys.platform not in compatable_os:
        logger.critical("FATAL_OS_NOT_SUPPORTED")
        return('FATAL_OS_NOT_SUPPORTED')
    logger.info('OK_OS_SUPPORTED')
    return('OK_OS_SUPPORTED')


def shell_check() -> str:
    compatable_shell: list[str] = ['bash', 'zsh', 'fish']
    shell_dir: str | None = os.environ.get("SHELL")
    if  shell_dir != None:
        shell_dir_split: list[str] = shell_dir.split('/')
    else:
        logger.critical('FATAL_NO_SHELL_FOUND')
        return('FATAL_NO_SHELL_FOUND')
    
    shell_list: str = shell_dir_split[-1]
    if  shell_list not in compatable_shell:
        logger.critical('FATAL_SHELL_NOT_SUPPORTED')
        return('FATAL_SHELL_NOT_SUPPORTED')
    logger.info('OK_SHELL_SUPPORTED')
    return('OK_SHELL_SUPPORTED')


def py_version_check() -> str:
    if  sys.version_info <= (3, 10):
        logger.critical('FATAL_PY_VER_NOT_SUPPORTED')
        return('FATAL_PY_VER_NOT_SUPPORTED')
    logger.info('OK_PY_VER_SUPPORTED')
    return ('OK_PY_VER_SUPPORTED')


def file_perms_check() -> str:
    pass
    

def base_checks() -> str :
    os_check_return: str = os_check()
    if  os_check_return.startswith("ERR_"):
        return os_check_return
    
    shell_check_return: str = shell_check()
    if  shell_check_return.startswith("ERR_"):
        return shell_check_return
    
    py_check_return : str = py_version_check()
    if  shell_check_return.startswith("ERR_"):
        return py_check_return
    
    return ('OK_ALL_CHECK_SUCCESS')


if  __name__ == "__main__":
    base_checks()
    print(os.environ.get("SHELL"))