import sys
import os
   
def os_check() -> str:
    compatable_os: list[str] = ["linux", "darwin"]
    if  sys.platform in compatable_os:
        return('OK_OS_SUPPORTED') #LOG 
    else:
        return('ERR_OS_NOT_SUPPORTED') #LOG

def shell_check() -> str:
    compatable_shell: list[str] = ['bash', 'zsh', 'fish']
    shell_dir: str | None = os.environ.get("SHELL")
    if  shell_dir != None:
        shell_dir_split: list[str] = shell_dir.split('/')
    else:
        return('ERR_NO_SHELL_FOUND') #LOG
    shell_list: str = shell_dir_split[-1]
    if  shell_list in compatable_shell:
        return('OK_SHELL_SUPPORTED') #LOG
    else:
        return('ERR_SHELL_NOT_SUPPORTED') #LOG

def base_checks() -> str :
    return_os_check: str = os_check()
    if  return_os_check.startswith("ERR_"):
        return return_os_check
    return_shell_check: str = shell_check()
    if  return_shell_check.startswith("ERR_"):
        return return_shell_check
    
    return ('OK_ALL_CHECK_SUCCESS')


if  __name__ == "__main__":
    base_checks()