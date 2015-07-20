# -*- coding: utf-8 -*-

import threading
import time
from datetime import datetime

t_cycle = 30 # ms

class ThreadGui(threading.Thread):

    def __init__(self, gui):
        threading.Thread.__init__(self)
        self.gui = gui

    def run(self):

        while(True):

            start_time = datetime.now()
            self.gui.update()
            end_time = datetime.now()

            dt = end_time - start_time
            dtms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            
            if(dtms < t_cycle):
                time.sleep((time_cycle - ms) / 1000.0);
