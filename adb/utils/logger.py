import logging

formatter = logging.Formatter(fmt='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                              datefmt='%d-%m-%Y:%H:%M:%S')
handler = logging.StreamHandler()
handler.setFormatter(formatter)


def get_logger(name):
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    return logger