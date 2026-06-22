import logging.config
from idk.core import bootstrap, history_collector, log_config, setup_wizard, history_cleaner
from idk.cli import cli


def main() -> None:

   cli.run()

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

   #read shell history from ./<shell>_history
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
   main()