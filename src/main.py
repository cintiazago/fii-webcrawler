import os
import logging
import logging.handlers

from crawlers import real_state_funds


APP_LOG_DIR = os.path.join('/'.join(
    os.path.dirname(
        os.path.abspath(__file__)).split('/')[:-1]),
            'logging')

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
    rotation_handler = logging.handlers.TimedRotatingFileHandler(
        APP_LOG_FILENAME, when='midnight', backupCount=7)
    rotation_handler.setFormatter(log_formatter)
    logger.addHandler(rotation_handler)
    logging.getLogger("requests").setLevel(logging.WARNING)

if __name__ == "__main__":
    config_log()
    logging.info('Starting application...')
    bot = real_state_funds.BotRealStateFunds()
    bot.start()
