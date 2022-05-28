import ulysses
from time import sleep

if __name__ == '__main__':
    # Get logger
    logger = ulysses.get_logger()

    while True:
        # Run main method then sleep for 5 minutes
        try:
            ulysses.main(logger)
        except Exception as e:
            logger.error(e)
        
        sleep(5 * 60)
