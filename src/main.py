import config
import logging
import logging.config

from mist.chaty import MistralChaty

# Initialize logging
logging.config.dictConfig(config.LOGGING_CONFIG)
logger = logging.getLogger(__name__)


from langfuse.callback import CallbackHandler
langfuse_handler = CallbackHandler(
    public_key="pk-lf-5ff3ee52-c399-4297-a8cd-7e82e539912f",
    secret_key="sk-lf-81b54566-d18d-494d-8c84-d5d0e31d2264",
    host="http://localhost:3000"
)

def main():

    try:
        config.validate_config()
        # Use configuration
        if config.DEBUG:
            logger.info(f"Running in {config.ENVIRONMENT} mode")
            logger.debug("Debug mode is enabled")

        chaty = MistralChaty()        
        chaty.chat(langfuse_handler)


    except KeyboardInterrupt:
        logger.info("\nOperation cancelled by user")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    logger.info("Application started")
    main()
