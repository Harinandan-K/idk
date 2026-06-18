import sys
import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

'''def install_req() -> str:
    req_file_path = Path(__file__).resolve().parent.parent / 'requirements.txt'
    if  not req_file_path.is_file():
        logger.error('ERR_REQ.TXT_MISSING')
        return('ERR_REQ.TXT_MISSING')
    logger.info('OK_REQ.TXT_FOUND')

    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(req_file_path)],
                                           capture_output=True,
                                           check=True,
                                           text=True
                                           )
        logger.info('OK_REQ_MODS_INSTALLED')
        return ('OK_REQ_MODS_INSTALLED')
            
    except subprocess.CalledProcessError as err:
        logger.error(f'ERR_PIP_MODULE_INSTALL_FAILED -> \n{err.stderr}')
        return ('ERR_PIP_MODULE_INSTALL_FAILED')'''
    

def setup_caller() -> str:
    
    return ('OK_SETUP_WIZARD_SUCCESS')


if  __name__ == '__main__':
    setup_caller()
    print(Path(__file__).resolve().parent.parent / 'requirements.txt')