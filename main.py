import logging.config
from core import bootstrap,log_config


def main() -> None:

   #setting up the logger
   logging.config.dictConfig(log_config.LOGGING_CONFIG)
   logger = logging.getLogger(__name__)
   logger.info("Logging succefully started!")

   #peeform the base_check 
   base_check: str = bootstrap.base_checks()
   if  base_check.startswith('ERR_'):
      logger.debug("Need to pass the ERR cli module")
      logger.error(base_check)
   
   logger.info(base_check)

if __name__ == "__main__":
   main()
   