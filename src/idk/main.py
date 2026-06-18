import logging.config
from idk.core import bootstrap, log_config, setup_wizard, history_reader


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


   #setup wizard round 1
   setup_caller_return: str = setup_wizard.setup_caller()
   if  setup_caller_return.startswith('FATAL_'):
      logger.debug('Need to pass the ERR cli module')
   else:
      logger.info(setup_caller_return)

   #read shell histrory from ./<shell>_history
   history_reader_return: str = history_reader.history_read()
   if  history_reader_return.startswith('FATAL_'):
      logger.debug('Need to pass the ERR cli module')
   else:
      logger.info(history_reader_return)

   #filter shell history (src/idk/etc/raw_shell_history.txt)



if __name__ == '__main__':
   main()
   