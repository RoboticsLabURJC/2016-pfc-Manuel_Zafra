#!/usr/bin/env python3

import sys
import signal
from PyQt4 import QtGui
from gui.gui import Gui
from gui.threadgui import ThreadGui
from interfaces.interfaces import Interfaces
from interfaces.threadint import ThreadInt
from pilot.pilot import Pilot
from pilot.threadpilot import ThreadPilot


signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    interface = Interfaces()

    window = Gui()
    window.setInterface(interface)
    window.show()

    pilot = Pilot(interface)

    t1 = ThreadInt(interface)  
    t1.start()

    t2 = ThreadGui(window)  
    t2.start()

    t3 = ThreadPilot(pilot)  
    t3.start()


    sys.exit(app.exec_())

