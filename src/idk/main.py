import logging.config
from idk.core import bootstrap,log_config, setup_wizard


def main() -> None:

   #setting up the logger
   logging.config.dictConfig(log_config.LOGGING_CONFIG)
   logger = logging.getLogger(__name__)
   logger.info("Logging succefully started")

   #perform the base_check 
   base_check_return: str = bootstrap.base_checks()
   if  base_check_return.startswith('ERR_'):
      logger.debug("Need to pass the ERR cli module")
      logger.error(base_check_return)
   else:
      logger.info(base_check_return)

   #setup wizard (runs if new install)
   setup_caller_return: str = setup_wizard.setup_caller()
   if  setup_caller_return.startswith('ERR_'):
      logger.debug("Need to pass the ERR cli module")
      logger.error(setup_caller_return)
   else:
      logger.info(setup_caller_return)


if __name__ == "__main__":
   main()
   