"""
primary.py - Perform the primary experiment
Author: Joe Bell
"""

import time
import logging

import atmos  # pip it

import animations
import datalogger
import animated_sense_hat

def get_abs_humidity(sense):
    """Get the absolute humidity,
    handles unit conversions(why does sense hat not use SI units?)"""

    # Get relative humidity
    relh = sense.get_humidity()

    # Get pressure, and convert from mB to Pa
    pressure = sense.get_pressure() * 100

    # Get temperature, and convert from degrees Celsius to kelvin
    temp = sense.get_temperature() + 273.15

    # Get absolute humidity
    abshumidity = atmos.calculate("AH", RH=relh, T=temp, p=pressure)

    # Why is the SI unit the KILOgram?
    return abshumidity * 1000

def take_baseline(sense):
    """Take a baseline(sample of normal values)"""
    # Show appropriate animation.
    sense.show_animation(animations.baseline)
    measurements = []
    for _ in range(5):
        measurements.append(get_abs_humidity(sense))
        time.sleep(5)
    avg = sum(measurements)/len(measurements)
    valrange = max((max(measurements) - min(measurements), 0.2))
    if valrange > 5:
        avg, valrange = take_baseline(sense)
    sense.show_animation(animations.astronaut_away)
    return avg, valrange

def run_experiment(duration, sense: animated_sense_hat.AnimatedSenseHat):
    """Runs the primary experiment, given its duration in minutes"""
    logger = logging.getLogger("SmileyPi.primary")
    logger.info("Starting Experiment")

    datalog = datalogger.DataLogger("primary", ["timestamp", "humidity", "astronaut"])

    # Convert to seconds, and then take away half minute for innacuracy
    duration = (duration * 60) - 30
    start_time = int(time.time()) # Get start time

    sense.show_animation(animations.baseline)
    avg, valrange = take_baseline(sense)
    astronaut = prev_astronaut = False
    logger.debug("Avg: " + str(avg) + ", Range: "+ str(valrange))
    while True:
        humidity = get_abs_humidity(sense)
        logger.debug("Humidity: " + str(humidity))
        astronaut = humidity > (avg + 1.5*valrange)

        timestr = time.strftime("%Y-%m-%d %H:%M:%S")
        datalog.writerow(timestamp=timestr, humidity=humidity, astronaut=int(astronaut))

        if astronaut and not prev_astronaut:
            logger.info("Astronaut Detected")
            sense.show_animation(animations.astronaut_here)
        elif not astronaut and prev_astronaut:
            logger.info("Astronaut Left")
            sense.show_animation(animations.astronaut_away)

        if humidity < (avg - valrange):
            logger.info("Retaking Baseline")
            avg, valrange = take_baseline(sense)
            astronaut = False

        if int(time.time()) >= (start_time + duration):
            logger.info("Experiment Time Finished")
            break

        prev_astronaut = astronaut
        time.sleep(10)
    datalog.close()
