#! /usr/bin/python

import sys
import Ice
import signal
import time
from PyQt4 import QtGui
from gui.gui import Gui as g
from gui.threadgui import ThreadGui as thg
from control.control import Control as ctrl
from control.threadcontrol import ThreadControl as thctrl

signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    control = ctrl.Control()
    gui = g.Gui()

    gui.show()

    t1 = ThreadControl(control)  
    t1.start()
    
    t2 = ThreadGUI(gui)  
    t2.start()

    sys.exit(status)
