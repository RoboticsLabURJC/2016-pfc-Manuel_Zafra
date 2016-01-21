#! /usr/bin/python

import sys
from PyQt4 import QtGui
from gui.gui import Gui
from gui.threadgui import ThreadGui
from control.control import Control
from control.threadcontrol import ThreadControl
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == '__main__':

    control = Control()

    app = QtGui.QApplication(sys.argv)

    window = Gui()
    window.setControl(control)
    window.show()

    t1 = ThreadControl(control)  
    t1.start()
    
    t2 = ThreadGui(window)  
    t2.start()

    sys.exit(app.exec_())

