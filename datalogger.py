import csv
import time

class DataLogger:
    def __init__(self, name, columns):
        # Put the date into a readble string
        datestr = time.strftime("--%Y-%m-%d--%H-%M")
        # Form the file's path
        self.filename = "data/" + name + datestr + ".csv"
        # Open the file for writing
        self.file = open(filename, "w")
        # Use the wonders of the csv library
        self.writer = csv.DictWriter(self.file, fieldnames = columns)
        self.writer.writeheader()

    def writerow(self, **kwargs):
        # Don't you think kwargs is a silly word?
        # Write a row in the csv file, columns are the parameter name, value is value
        self.writer.writerow(kwargs)

    def close(self):
        # Explicitly close the csv file
        self.file.close()
    def __del__(self):
        # Close file when object is deleted(unreliable)
        self.close()
    def __exit__(self, *args):
        # Close file when leaving 'with' block
        self.close()
