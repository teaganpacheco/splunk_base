# Standard library imports
import logging
import logging.handlers
import os
import datetime as dt

# Splunk imports
from splunk.appserver.mrsparkle.lib.util import make_splunkhome_path
import time


class CustomFormatter(logging.Formatter):

    converter = dt.datetime.fromtimestamp

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%m-%d-%Y %H:%M:%S")
            print(t)
            print(record.msecs)
            s = "%s.%03d" % (t, record.msecs)
            print(s)

        return s

def setup_logging(log_name, log_level=logging.INFO):
    """ Setup logger.

    :param log_name: name for logger
    :param log_level: log level, a string
    :return: a logger object
    """

    app_log_dir = make_splunkhome_path(["var", "log", "python_upgrade_readiness_app"])

    if not os.path.exists(app_log_dir):
        os.makedirs(app_log_dir)

    skynet_log_dir = make_splunkhome_path(["var", "log", "python_upgrade_readiness_app", "scan_summary"])
    if not os.path.exists(skynet_log_dir):
        os.makedirs(skynet_log_dir)

    log_file = make_splunkhome_path(["var", "log", "python_upgrade_readiness_app", "scan_summary", "%s.log" % log_name])

    logger = logging.getLogger(log_name)
    logger.propagate = False

    # Set log level
    logger.setLevel(log_level)

    handler_exists = any([True for h in logger.handlers if h.baseFilename == log_file])

    if not handler_exists:
        file_handler = logging.handlers.RotatingFileHandler(log_file, mode="a", maxBytes=10485760, backupCount=10)
        # Format logs
        fmt_str = "%(asctime)s %(levelname)s jQueryScanSummary - %(message)s"
        formatter = logging.Formatter(fmt_str, datefmt='%m-%d-%Y %H:%M:%S %z')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        if log_level is not None:
            file_handler.setLevel(log_level)

    return logger
