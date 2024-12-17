import config
import logging
import logging.config

from mist.chaty import MistralChaty

# Initialize logging
logging.config.dictConfig(config.LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def main():
    try:
        config.validate_config()
        # Use configuration
        if config.DEBUG:
            logger.info(f"Running in {config.ENVIRONMENT} mode")
            logger.debug("Debug mode is enabled")

        chaty = MistralChaty()        
        chaty.chat()


    except KeyboardInterrupt:
        logger.info("\nOperation cancelled by user")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    logger.info("Application started")
    main()
