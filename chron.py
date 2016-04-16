import time
from threading import *

class Chronometer(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event
        self.daemon = True
        #self.stopped.set()
        self.time = 0

    def run(self):
        while True:
            if not self.stopped.wait(0.99):
                self.time += 1
                #print "test"
            else:
                pass
            # call a function
