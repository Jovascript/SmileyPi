# SmileyPi
### An entry to the Astro Competition's 2nd Phase

## Running
### Dependencies
This installation might be a little tricky, but:

 - Python 3.2+
 - pyephem (via pip)
 - atmos (via pip)
 - Of course, the sense_hat library

This is complicated by the fact that, for some reason, pip3 stops working:(Cannot import packaging.version)
This may be allieviated by:
```sudo -i
apt-get purge -y python3-pip
wget https://bootstrap.pypa.io/get-pip.py
python3 ./get-pip.py
apt-get install python3-pip
```
This is not our fault, or anyone's, so bear this in mind if the code does not work.


### Execution
To execute the experiment, simply run `python3 SmileyPi.py` **in the SmileyPi directory**

It will deposit the data files, in csv format, in the `data` directory, and logs in the `logs` directory.

## Testing
### Whole Script
Simply run SmileyPi.py, with python 3.
Make sure you did `pip3 install -r requirements.txt` first.
It will run both experiments.

### Primary Experiment
You can test it by running `python3 SmileyPi.py primary`
It should:

 - Detect when a human is in a room
 - It should start, take a baseline, and then test for a rise in humidity.
 - If you were in the room to start with, when you leave it should retake baseline if humidity goes down.

### Secondary Experiment
You can test it by running `python3 SmileyPi.py secondary`.
It should:

- Calculate when ISS is in shadow, umbra or penumbra.
- Calculate a 'light intensity' percentage.
- Log this along with the time and temperature.
