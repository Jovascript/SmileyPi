"""Runs the secondary experiment"""
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

    for _ in range(num_loops):
        temperature = sense.get_temperature()
        datestr = time.strftime("%Y-%m-%d %H:%M:%S")
        light = shadow.get_light_intensity()
        datalog.writerow(timestamp=datestr, temp=temperature, light_intensity=light)

        if light == 100 and anim != animations.sun_full:
            anim = animations.sun_full
            sense.show_animation(anim)
        elif light > 0 and anim != animations.sunrise:
            anim = animations.sunrise
            sense.show_animation(anim)
        elif anim != animations.night:
            anim = animations.night
            sense.show_animation(anim)

        time.sleep(measurement_freq)

    logger.info("Completed Secondary Experiment")
    datalog.close()
