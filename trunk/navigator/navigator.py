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

    if not ( (len(sys.argv) == 3)
        and ((sys.argv[2] == 'sim') or (sys.argv[2] == 'real')) ):

        print (sys.argv[2])
        print ('Usage: navigator [iceconf.cfg] [sim|real]')
        sys.exit()

    app = QtGui.QApplication(sys.argv)

    interface = Interfaces(sys.argv[2])

    window = Gui(sys.argv[2])
    window.setInterface(interface)
    window.show()

    pilot = Pilot(interface, sys.argv[2])

    t1 = ThreadInt(interface)  
    t1.start()

    t2 = ThreadGui(window)  
    t2.start()

    t3 = ThreadPilot(pilot)  
    t3.start()


    sys.exit(app.exec_())

