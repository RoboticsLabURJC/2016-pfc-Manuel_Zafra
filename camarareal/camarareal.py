#! /usr/bin/python

import sys
import Ice
import signal
import time
from PyQt4 import QtGui
from gui.gui import Gui
from gui.threadgui import ThreadGui
from control.control import Control
from control.threadcontrol import ThreadControl

signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == '__main__':

    #app = QtGui.QApplication(sys.argv)
    ice = Ice.initialize()

    control = Control(ice)
    gui = Gui()

    gui.show()

    t1 = ThreadControl(control)  
    t1.start()
    
    t2 = ThreadGUI(gui)  
    t2.start()

    sys.exit(status)
