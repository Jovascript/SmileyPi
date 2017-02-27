"""
secondary.py - Runs the secondary experiment
Author: Joe Bell
"""

import time
import logging
import os


import datalogger
import shadow
import animations

def get_cpu_temp():
    # Excecutes vcgencmd to find CPU temp
    res = os.popen('vcgencmd measure_temp').readline()
    return float(res.replace("temp=", "").replace("'C\n", ""))

def get_corrected_temp(sense):
    """Corrects temperature to account for CPU heat."""
    temp = sense.get_temperature()
    cpu_temp = get_cpu_temp()
    # Uses magic factor to correct measured temp
    # Source: github.com/initialstate/wunderground-sensehat/wiki/Part-3.-Sense-HAT-Temperature-Correction
    return temp - ((cpu_temp - temp)/5.466)


def run_experiment(duration, measurement_freq, sense):
    '''Run the experiment, give the duration in minutes,
    and how often to take measurements(in seconds)'''

    # Initialise Datalogger, and logger
    datalog = datalogger.DataLogger("secondary", ["timestamp", "temp", "light_intensity"])
    logger = logging.getLogger("SmileyPi.secondary")

    # Number of times to run loop, convert minutes into seconds and divide.
    num_loops = int((duration*60)/measurement_freq)
    logger.info("Running %d times, waiting %d seconds each run.", num_loops, measurement_freq)

    for i in range(num_loops):
        # Get more accourate temperature.
        temperature = get_corrected_temp(sense)
        # Format datetime into string
        datestr = time.strftime("%Y-%m-%d %H:%M:%S")
        # Get the light intensity(from shadow calcs)
        light = shadow.get_light_intensity()
        # Write data to csv file.
        datalog.writerow(timestamp=datestr, temp=temperature, light_intensity=light)

        logger.debug("Light Intensity: " + str(light))

        if light == 100:
            # If in full sunlight
            sense.show_animation(animations.sun_full)
        elif light > 0:
            # If in partial sunlight
            sense.show_animation(animations.sunrise)
        else:
            # In complete shadow
            sense.show_animation(animations.night)

        # Sleep for right amount of time.
        time.sleep(measurement_freq)

    logger.info("Completed Secondary Experiment")
    datalog.close()
