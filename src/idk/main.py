import logging.config
<<<<<<< HEAD
from idk.core import bootstrap,log_config, setup_wizard
=======
from idk.core import bootstrap, history_collector, log_config, setup_wizard, history_cleaner
>>>>>>> 803604ee6976fdf3adf084860a4e5f9118d50edc


def main() -> None:

   #setting up the logger
   logging.config.dictConfig(log_config.LOGGING_CONFIG)
   logger = logging.getLogger(__name__)
<<<<<<< HEAD
   logger.info("Logging successfully started")

   #perform the base_check 
   base_check_return: str = bootstrap.base_checks()
   if  base_check_return.startswith('FATAL_'):
      logger.debug("Need to pass the ERR cli module")
   else:
      logger.info(base_check_return)

   #setup wizard (runs if new install)
   setup_caller_return: str = setup_wizard.setup_caller()
   if  setup_caller_return.startswith('FATAL_'):
      logger.debug("Need to pass the ERR cli module")
   else:
      logger.info(setup_caller_return)


if __name__ == "__main__":
=======
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
   history_collector_return: str = history_collector.history_collector()
   if  history_collector_return.startswith('FATAL_'):
      logger.debug('Need to pass the ERR cli module')
   else:
      logger.info(history_collector_return)

   #filter shell history (src/idk/etc/raw_shell_history.txt)
   history_cleaner_return: str = history_cleaner.history_cleaner()
   if  history_cleaner_return.startswith('FATAL_'):
      logger.debug('Need to pass the ERR cli module')
   else:
      logger.info(history_cleaner_return)

if __name__ == '__main__':
>>>>>>> 803604ee6976fdf3adf084860a4e5f9118d50edc
   main()
   