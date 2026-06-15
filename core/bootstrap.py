import os
import sys
import logging

logger = logging.getLogger(__name__)


def os_check() -> str:
    compatable_os: list[str] = ["linux", "darwin"]
    if  sys.platform not in compatable_os:
        logger.error("ERR_OS_NOT_SUPPORTED")
        return('ERR_OS_NOT_SUPPORTED')
    logger.info('OK_OS_SUPPORTED')
    return('OK_OS_SUPPORTED')


def shell_check() -> str:
    compatable_shell: list[str] = ['bash', 'zsh', 'fish']
    shell_dir: str | None = os.environ.get("SHELL")
    if  shell_dir != None:
        shell_dir_split: list[str] = shell_dir.split('/')
    else:
        logger.error('ERR_NO_SHELL_FOUND')
        return('ERR_NO_SHELL_FOUND')
    
    shell_list: str = shell_dir_split[-1]
    if  shell_list not in compatable_shell:
        logger.error('ERR_SHELL_NOT_SUPPORTED')
        return('ERR_SHELL_NOT_SUPPORTED')
    logger.info('OK_SHELL_SUPPORTED')
    return('OK_SHELL_SUPPORTED')


def py_version_check() -> str:
    if  sys.version_info <= (3, 10):
        logger.error('ERR_PY_VER_NOT_SUPPORTED')
        return('ERR_PY_VER_NOT_SUPPORTED')
    logger.info('OK_PY_VER_SUPPORTED')
    return ('OK_PY_VER_SUPPORTED')
    

def base_checks() -> str :
    return_os_check: str = os_check()
    if  return_os_check.startswith("ERR_"):
        return return_os_check
    
    return_shell_check: str = shell_check()
    if  return_shell_check.startswith("ERR_"):
        return return_shell_check
    
    return_py_check: str = py_version_check()
    if  return_shell_check.startswith("ERR_"):
        return return_py_check
    
    return ('OK_ALL_CHECK_SUCCESS')


if  __name__ == "__main__":
    base_checks()
    print(os.environ.get("SHELL"))