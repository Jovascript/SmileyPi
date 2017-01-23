"""Perform the primary experiment
@author = Joe Bell"""
import time
import logging

import atmos  # pip it
import sense_emu


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
    sense.clear(0, 0, 255)
    measurements = []
    for _ in range(5):
        measurements.append(get_abs_humidity(sense))
        time.sleep(5)
    avg = sum(measurements)/len(measurements)
    valrange = max(measurements) - min(measurements)
    return avg, valrange

def run_experiment(duration):
    """Runs the primary experiment, given its duration in minutes"""
    sense = sense_emu.SenseHat()
    logger = logging.getLogger("Primary")
    num_loops = duration*6 # Get duration in seconds (*60) and divide by 10, for loops.
    num_loops -= (5) # Take away some loops to estimate baseline time consumption.
    avg, valrange = take_baseline(sense)
    astronaut = False
    for _ in range(num_loops):
        humidity = get_abs_humidity(sense)
        if humidity > (avg + 2*valrange):
            if not astronaut:
                astronaut = True
                logger.info("Astronaut Detected")
                sense.clear(0, 255, 0)
        else:
            sense.clear(255, 0, 0)
            if astronaut:
                astronaut = False
                logger.info("Astronaut Left")
            if humidity < (avg + 2*valrange):
                logger.info("Retaking Baseline")
                avg, valrange = take_baseline(sense)
        time.sleep(10)
if __name__ == "__main__":
    run_experiment(10)
    