import logging
from bot.configuration import bot, logger

if __name__ == '__main__':
    logger.info("=" * 50)
    logger.info("Запуск бота...")
    logger.info("=" * 50)

    try:
        logger.info("Запуск polling бота (режим non-stop)")
        bot.polling(non_stop=True, timeout=60)
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем (KeyboardInterrupt)")
    except Exception as e:
        logger.critical(f"Бот упал с ошибкой: {e}", exc_info=True)
        raise
    finally:
        logger.info("Завершение работы бота")
