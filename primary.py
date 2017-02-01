"""Perform the primary experiment
@author = Joe Bell"""
import time
import logging

import atmos  # pip it

import animations
import animated_sense_hat

def get_abs_humidity(sense):
    """Get the absolute humidity,
    handles unit conversions(why does sense hat not use SI units?)"""

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
    valrange = max(measurements) - min(measurements)
    sense.show_animation(animations.astronaut_away)
    return avg, valrange

def run_experiment(duration, sense: animated_sense_hat.AnimatedSenseHat):
    """Runs the primary experiment, given its duration in minutes"""
    logger = logging.getLogger("SmileyPi.primary")
    logger.info("Starting Experiment")

    num_loops = duration*6 # Get duration in seconds (*60) and divide by 10, for loops.
    num_loops -= (5) # Take away some loops to estimate baseline time consumption.

    sense.show_animation(animations.baseline)
    avg, valrange = take_baseline(sense)
    astronaut = prev_astronaut = False
    logger.debug("Avg: " + str(avg) + ", Range: "+ str(valrange))
    for _ in range(num_loops):
        humidity = get_abs_humidity(sense)
        logger.debug("Humidity: " + str(humidity))
        astronaut = humidity > (avg + valrange)

        if astronaut and not prev_astronaut:
            logger.info("Astronaut Detected")
            sense.show_animation(animations.astronaut_here)
        elif not astronaut and prev_astronaut:
            logger.info("Astronaut Left")
            sense.show_animation(animations.astronaut_away)

        if humidity < (avg - 2*valrange):
            logger.info("Retaking Baseline")
            avg, valrange = take_baseline(sense)
            astronaut = False

        prev_astronaut = astronaut
        time.sleep(10)
