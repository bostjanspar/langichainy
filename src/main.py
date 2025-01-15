import logging
import logging.config

#MY CODE
import config

# Initialize logging
logging.config.dictConfig(config.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def main():

    try:
        logger.info(f"Running in {config.ENVIRONMENT} mode")
        # Use configuration
        if config.DEBUG:  
            logger.debug("Debug mode is enabled")
        

    except KeyboardInterrupt:
        logger.info("\nOperation cancelled by user")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    logger.info("Application started")
    main()
