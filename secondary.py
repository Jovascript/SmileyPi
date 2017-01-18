import time
import logging

import sense_emu

import datalogger
import shadow


def run_experiment(time, measurement_freq):
    '''Run the experiment, give the duration in minutes, and how often to take measurements(in seconds)'''
    datalog = datalogger.DataLogger("secondary", ["timestamp", "temp", "light_intensity"])
    logger = logging.getLogger("Secondary")
    sense = sense_emu.SenseHat()
    num_loops = int((time*60)/measurement_freq) # Number of times to run loop, convert minutes into seconds and divide.
    logger.info("Running %d times, waiting %d seconds each run.", num_loops, measurement_freq)
    for i in range(num_loops):
        temperature = sense.get_temperature()
        datestr = time.strftime("%Y-%m-%d %H:%M:%S")
        light = shadow.get_light_intensity()
        datalog.writerow(timestamp=datestr, temp=temperature, light_intensity=light)
        time.sleep(measurement_freq)
    logger.info("Completed Secondary Experiment")
    datalog.close()