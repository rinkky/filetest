#!/usr/bin/env python
# coding=utf-8

import logging
import os
import re
import threading
import time

class LogStream(object):
    """stream can be used for log handler
    """

    def __init__(self, queue):
        self._queue = queue

    def write(self, msg):
        self._queue.put(msg)

    def flush(self):
        pass

class TestLog(object):
    """create and save test log

    """

    PASS_FLAG = "[PASSED]"
    FAIL_FLAG = "[FAILED]"
    END_FLAG = "[END]"
    BEGIN_FLAG = "[BEGIN]"
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
        logger.addHandler(log_handler)
        self._logger = logger

    def passlog(self, file_name, log_msg):
        """put pass log into stream

        Args:
            file_name: tested file

        """
        self._logger.info(
            "{0} - {1}: {2}".format(
                self.PASS_FLAG, 
                os.path.basename(file_name), 
                log_msg
            )
        )

    def errorlog(self, file_name, log_msg):
        """put error log into stream

        Args:
            file_name: tested file
            log_msg: why not this file pass the test
        """
        self._logger.error(
            "{0} - {1}: {2}".format(
                self.FAIL_FLAG, 
                os.path.basename(file_name), 
                log_msg
            )
        )

    def normallog(self, log_msg):
        """any msg

        """
        self._logger.info(log_msg)
        
    def test_equal(self, a, b, file_name, log_msg):
        """if a == b then pass, else fail
        
        """
        if(a == b):
            self.passlog(os.path.basename(file_name), log_msg)
            return True
        else:
            self.errorlog(os.path.basename(file_name), log_msg)
            return False

    def test_bigger(self, a, b, file_name, log_msg):
        """if a > b then pass, else fail

        """
        if(a > b):
            self.passlog(os.path.basename(file_name), log_msg)
            return True
        else:
            self.errorlog(os.path.basename(file_name), log_msg)
            return False

    def test_true(self, is_true, file_name, log_msg):
        """if is_true then pass, else fail

        """
        if(is_true):
            self.passlog(os.path.basename(file_name), log_msg)
            return True
        else:
            self.errorlog(os.path.basename(file_name), log_msg)
            return False

class LogThread(threading.Thread):
    """the thread to handle logs
    
    print log to screen, and save them.
    if you want do more, make your own log thread.
    logs are cached in log_queue.
    """
    def __init__(self, log_queue, log_file, fail_only=True):
        threading.Thread.__init__(self)
        self._log_queue = log_queue
        self.log_file = log_file
        self.file_stream = open(log_file, "a")
        self.daemon = True
        self.fail_only = fail_only

    def run(self):
        while True:
            if(self._log_queue.empty()):
                time.sleep(1)
                continue
            log = self._log_queue.get(False)
            print(log)
            if(self.fail_only == True and log.startswith("[PASS]")):
                continue
            self.file_stream.write(log+"\n")
            if(log.startswith("[end]")):
                break
        self.file_stream.close()
