from adb.utils.logger import AdbLogging
import logging

def test_without_logging(capsys):
    logger = AdbLogging.get_logger("adb.test")
    logger.addHandler(logging.StreamHandler())

    logger.info("INFO message")
    captured = capsys.readouterr()
    assert not captured.out
    assert not captured.err

    logger.warning("WARNING message")
    captured = capsys.readouterr()
    assert not captured.out
    assert not captured.err

    logger.debug("DEBUG message")
    assert not captured.out
    assert not captured.err

def test_without_log_message_after_set_root_logger_level(capsys):
    logger = AdbLogging.get_logger("adb.test")
    logger.addHandler(logging.StreamHandler())

    logging.getLogger().setLevel(logging.DEBUG)

    logger.info("INFO message")
    captured = capsys.readouterr()
    assert not captured.out
    assert not captured.err

    logger.warning("WARNING message")
    captured = capsys.readouterr()
    assert not captured.out
    assert not captured.err

    logger.debug("DEBUG message")
    assert not captured.out
    assert not captured.err
