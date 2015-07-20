import threading
import time
from datetime import datetime

t_cycle = 60 # ms

class ThreadControl(threading.Thread):

    def __init__(self, control):
        threading.Thread.__init__(self)
        self.control = control

    def run(self):

        start_time = datetime.now()
        self.control.update()
        end_time = datetime.now()

        dt = end_time - start_time
        dtms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            
        if(dtms < t_cycle):
            time.sleep((time_cycle - ms) / 1000.0);
