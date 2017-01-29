""" A subclass of sense hat for running the sense hat animations."""
import threading
import time
from queue import Queue

from sense_hat import SenseHat


class AnimatedSenseHat(SenseHat):
    """Handles threaded animation runner."""
    def __init__(self, imu_settings_file='RTIMULib', text_assets='sense_hat_text'):
        super().__init__(self, imu_settings_file, text_assets)
        self.queue = Queue() # A thread-safe data interchange?
        # I hope

        self.thread = threading.Thread(target=self.run_animator)
        self.thread.start()

    def show_animation(self, animation):
        """Changes the animation running(threadsafe)"""
        self.queue.put(animation)

    def halt_animations(self):
        """Sends the message to close the animation thread"""
        self.queue.put("HALT")

    def run_animator(self):
        """The thread for animations"""
        status = "standby"
        i = 0
        while status != "HALT":
            if status != "standby":
                if i >= len(status):
                    i = 0
                self.set_pixels(status[i])
                i += 1
            time.sleep(1)
            if not self.queue.empty():
                # We ingore the risk that the queue might be changed in this time.
                # This (should) be the only thread accessing it.
                status = self.queue.get()
