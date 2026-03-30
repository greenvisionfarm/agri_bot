import logging
from bot.configuration import bot, logger

if __name__ == '__main__':
    logger.info("=" * 50)
    logger.info("Bot starting...")
    logger.info("=" * 50)
    
    try:
        logger.info("Starting bot polling (non-stop mode)")
        bot.polling(non_stop=True, timeout=60)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (KeyboardInterrupt)")
    except Exception as e:
        logger.critical(f"Bot crashed with error: {e}", exc_info=True)
        raise
    finally:
        logger.info("Bot shutdown complete")
