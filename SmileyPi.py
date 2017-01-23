import logging
import os
import time


def setupLogger():
    # create logger with correct name
    logger = logging.getLogger('SmileyPi')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fname = "logs/SmileyPiLog" + time.strftime("--%Y-%m-%d--%H-%M") + ".log"
    fh = logging.FileHandler(fname)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

def prepareDirs():
    # Creates dirs if they don't exist, only for python 3.2+
    os.makedirs("logs", exist_ok=True)
    os.makedirs("data", exist_ok=True)

# How long the experiment will last, and the script will run, in hours.
logger = setupLogger()
logger.info("Hi")
