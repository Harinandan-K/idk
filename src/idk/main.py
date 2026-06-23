import logging.config
from pathlib import Path
#from idk.cli import cli
#from idk.db import create_db
from idk.core import bootstrap, history_collector, log_config, history_cleaner

def main() -> None:

   #setting up the logger
   logging.config.dictConfig(log_config.LOGGING_CONFIG)
   logger = logging.getLogger(__name__)
   logger.info('INFO_LOGGING_STARTED')
   logger.info('INFO_LOGGING_MAIN')

   #perform the base_check 
   base_check_return: str = bootstrap.base_checks()
   if  base_check_return.startswith('ERR_') or base_check_return.startswith('WARN_') or base_check_return.startswith('FATAL_'):
      logger.critical(base_check_return)
      logger.debug('Need to pass the ERR cli module')
   else:
      logger.info(base_check_return)


   # check for first install run
   if not  (Path(__file__).resolve().parent.parent / 'db' / 'IDK_USER.db').exists():
      logger.debug("DEBUG_FIRST_RUN_TEST")


      #create DB
      logger.error('ERR_VARIBLE_MISSMATCH -> updated all upper case varibles are not updated in the codes fomr line 39 to 45')
      '''create_db_return = create_db.init_db()
      if  create_db_return.startswith('FATAL_'):
         logger.debug('Need to pass the ERR cli module')
      else:
         logger.info(create_db_return)'''
      
      logger.error('ERR_MISSING_EXPECTED_RETURN -> main.py expects a return of the code stats (OK_, ERR_, FATAL_) from /idk/db/create.db')
      logger.debug('INFO_DEL_ERROR_LOG -> if the errors are fixed delete the code line for error {ERR_VARIBLE_MISSMATCH} & {ERR_MISSING_EXPECTED_RETURN}. Also del ONLY this debug log code ')
      
      
      #cli call for first run -> welcome msg



      #read shell history
      history_collector_return: str = history_collector.history_collector()
      if  history_collector_return.startswith('FATAL_'):
         logger.debug('Need to pass the ERR cli module')
      else:
         logger.info(history_collector_return)

      #clean shell history
      history_cleaner_return: str = history_cleaner.history_cleaner()
      if  base_check_return.startswith('ERR_') or history_cleaner_return.startswith('FATAL_'):
         logger.debug('Need to pass the ERR cli module')
      else:
         logger.info(history_cleaner_return)

      #push the clean history to db
   

if __name__ == '__main__':
   main()