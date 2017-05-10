#!/usr/bin/env python
# coding=utf-8

import logging

class LogStream(object):
    """stream can be used for log handler
    """

    def __init__(queue):
        self._queue = queue

    def write(msg):
        self._queue.put(msg)

    def flush():
        pass

class TestLog(object):
    """create and save test log

    """

    def __init__(self, log_queue, logger_name):
        """init TestLog

        Args:
            log_queue: loger will put all log msg in this queue. 
            logger_name: name of the logger
            log_path: log will be saved to this path
        """
        self._queue = log_queue

        log_stream = LogStream(log_queue)
        log_handler = logging.StreamHandler(stream=log_stream)
        log_handler.setLevel(logging.DEBUG)
        log_handler.setFormatter(
            logging.Formatter(
                "%(message)s"
            )
        )

        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.addHander(log_handler)
        self._logger = logger

    def passlog(self, file_name, log_msg):
        """put pass log into stream

        Args:
            file_name: tested file

        """
        self._logger.info("[PASS] - {0}: {1}".format(file_name, log_msg))

    def errorlog(self, file_name, log_msg):
        """put error log into stream

        Args:
            file_name: tested file
            log_msg: why not this file pass the test
        """
        self._logger.error("[ERROR] - {0}: {1}".format(file_name, log_msg))

    def normallog(self, log_msg):
        """

        """
        self._logger.info(log_msg)
        