""" A subclass of sense hat for running the sense hat animations."""
import threading
import time
from queue import Queue

from sense_hat import SenseHat


class AnimatedSenseHat(SenseHat):
    """Handles threaded animation runner."""
    def __init__(self, lighting=True, imu_settings_file='RTIMULib', text_assets='sense_hat_text'):
        super().__init__(imu_settings_file, text_assets)
        self.queue = Queue() # A thread-safe data interchange?
        # I hope

        self.thread = threading.Thread(target=self.run_animator)
        # If it should do lighting, start animation thread
        if lighting:
            self.thread.start()

    def show_animation(self, animation):
        """Changes the animation running(threadsafe)"""
        # Add the animation change to the queue.
        self.queue.put(animation)

    def halt_animations(self):
        """Sends the message to close the animation thread"""
        # Add the HALT command to the queue.
        self.queue.put("HALT")

    def run_animator(self):
        """The thread for animations"""
        # The current status of the animator.
        status = "standby"
        # Current frame in animation
        i = 0
        # While it has not recieved the HALT command
        while status != "HALT":
            # and is not on standby
            if status != "standby":
                # Loop the frame back to 0 if its too large
                if i >= len(status):
                    i = 0
                # Set the pixels
                self.set_pixels(status[i])
                # Cycle to next frame
                i += 1
            # Pause
            time.sleep(1)
            # Check whether there is a new event in the queue
            if not self.queue.empty():
                # We ingore the risk that the queue might be changed in this time.
                # This (should) be the only thread accessing it.
                status = self.queue.get()
        # Clear the matrix when stopping thread.
        self.clear()
