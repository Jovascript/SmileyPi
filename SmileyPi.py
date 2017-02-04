"""
SmileyPi.py - Main file for running experiments
Author: Joe Bell
"""

import os
import sys
import time
import logging

from animated_sense_hat import AnimatedSenseHat
import primary, secondary

# ---CONFIG---
PRIMARY_DURATION = 90
SECONDARY_DURATION = 90
SECONDARY_MEASUREMENT_FREQUENCY = 5


def prepare_logger(name)->logging.Logger:
    """Setup logger"""
    # create logger with correct name
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fname = "logs/SmileyPiLog" + time.strftime("--%Y-%m-%d--%H-%M") + ".log"
    fh = logging.FileHandler(fname)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    log.addHandler(fh)
    log.addHandler(ch)
    return log

def prepare_dirs():
    "Creates dirs if they don't exist, only for python 3.2+"
    os.makedirs("logs", exist_ok=True)
    os.makedirs("data", exist_ok=True)

def run():
    """Run Experiment"""
    logger.info("Running Experiments")
    sense = AnimatedSenseHat()
    try:
        logger.info("Running Primary Experiment")
        primary.run_experiment(PRIMARY_DURATION, sense)
        logger.info("Running Secondary Experiment")
        secondary.run_experiment(SECONDARY_DURATION, SECONDARY_MEASUREMENT_FREQUENCY, sense)
    except KeyboardInterrupt:
        logger.info("STOPPED")
    sense.halt_animations()

def test(mytype):
    """Run test on specific part"""
    sense = AnimatedSenseHat()
    try:
        if mytype == "primary":
            primary.run_experiment(10, sense)
        else:
            secondary.run_experiment(10, 10, sense)
    except KeyboardInterrupt:
        logger.info("STOPPED")
    sense.halt_animations()

if __name__ == "__main__":
    prepare_dirs()
    logger = prepare_logger("SmileyPi")
    if len(sys.argv) > 1:
        if sys.argv[1] == "primary":
            test("primary")
        else:
            test("seconary")
    else:
        run()
