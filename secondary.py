"""
secondary.py - Runs the secondary experiment
Author: Joe Bell
"""

import time
import logging


import datalogger
import shadow
import animations


def run_experiment(duration, measurement_freq, sense):
    '''Run the experiment, give the duration in minutes,
    and how often to take measurements(in seconds)'''

    datalog = datalogger.DataLogger("secondary", ["timestamp", "temp", "light_intensity"])
    logger = logging.getLogger("SmileyPi.secondary")

    # Number of times to run loop, convert minutes into seconds and divide.
    num_loops = int((duration*60)/measurement_freq)
    logger.info("Running %d times, waiting %d seconds each run.", num_loops, measurement_freq)

    anim = animations.sun_full
    sense.show_animation(anim)

    for i in range(num_loops):
        temperature = sense.get_temperature()
        datestr = time.strftime("%Y-%m-%d %H:%M:%S")
        light = shadow.get_light_intensity()
        datalog.writerow(timestamp=datestr, temp=temperature, light_intensity=light)

        logger.debug(light)

        if light == 100:
            sense.show_animation(animations.sun_full)
        elif light > 0:
            sense.show_animation(animations.sunrise)
        else:
            sense.show_animation(animations.night)

        time.sleep(measurement_freq)

    logger.info("Completed Secondary Experiment")
    datalog.close()
