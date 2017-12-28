"""

This module contains Logger class.

"""
import logging

class Logger(object):
    """
    Logger class is used to records execution information.
    It wraps the Logger object from logging module which
    have two handlers: file handler and stream handler.
    5 logging levels are available: debug, info, warning, error, critial.
    For more information, see https://docs.python.org/3.6/library/logging.html .
    """
    LOG_DIR = './log'

    def __init__(self, name):
        import time
        import os
        # initialize
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)s]\t%(message)s')
        # file handler
        file_handler = logging.FileHandler(
            os.path.join(Logger.LOG_DIR, "{}_{}.log".format(
                name, int(time.time()))))
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        # stream handler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        # add handlers to the logger
        self._logger.addHandler(file_handler)
        self._logger.addHandler(stream_handler)

    def debug(self, msg):
        """
        Logs a message with level DEBUG on this logger

        :param msg: The message to record
        :return: None
        """
        self._logger.debug(msg)

    def info(self, msg):
        """
        Logs a message with level INFO on this logger

        :param msg: The message to record
        :return: None
        """
        self._logger.info(msg)

    def warning(self, msg):
        """
        Logs a message with level WARNING on this logger

        :param msg: The message to record
        :return: None
        """
        self._logger.warning(msg)

    def error(self, msg):
        """
        Logs a message with level ERROR on this logger

        :param msg: The message to record
        :return: None
        """
        self._logger.error(msg)

    def critical(self, msg):
        """
        Logs a message with level CRITICAL on this logger

        :param msg: The message to record
        :return: None
        """
        self._logger.critical(msg)
