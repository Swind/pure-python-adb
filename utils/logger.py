import logging
from logging.config import fileConfig

logging.getLogger("ppadb").setLevel(logging.CRITICAL)

class AdbLogging:

    @classmethod
    def get_logger(cls, name):
        fileConfig('logging_config.ini')
        logger = logging.getLogger()
        return logger
