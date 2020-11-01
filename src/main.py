import os
import logging
import logging.handlers

from crawlers import real_state_funds


APP_LOG_DIR = os.path.join('/'.join(
    os.path.dirname(
        os.path.abspath(__file__))
            .split('/')[:-1]), 'logging')

APP_LOG_FILENAME = 'main.log'


def config_log():
    log_level = getattr(logging, 'INFO', None)
    logger = logging.getLogger()
    log_formatter = logging.Formatter(
        "(%s) [%%(asctime)s] [%%(levelname)s] %%(message)s" % os.getpid())
    logger.setLevel(log_level)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    logger.addHandler(stream_handler)
    log_dir = APP_LOG_DIR
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)
    full_filename = os.path.join(log_dir, APP_LOG_FILENAME)
    rotation_handler = logging.handlers.TimedRotatingFileHandler(
        full_filename, when='midnight', backupCount=7)
    rotation_handler.setFormatter(log_formatter)
    logger.addHandler(rotation_handler)
    logging.getLogger("requests").setLevel(logging.WARNING)

if __name__ == "__main__":
    config_log()
    logging.info('Starting web crawler...')
    bot = real_state_funds.BotFIIsWebsite()
    bot.start()
