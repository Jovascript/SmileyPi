# SmileyPi
### An entry to the Astro Competition's 2nd Phase

## Testing
### Whole Script
Simply run SmileyPi.py, with python 3.
Make sure you did `pip3 install -r requirements.txt` first.
It will run both experiments.

### Primary Experiment
You can test it by running primary.py.
It should:

 - Detect when a human is in a room
 - It should start, take a baseline, and then test for a rise in humidity.
 - If you were in the room to start with, when you leave it should retake baseline if humidity goes down.

### Secondary Experiment
This will log data to a data directory.
It should calculate when the ISS is in shadow, and record that, as well as the temperature of the air.

