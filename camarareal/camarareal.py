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
    print 'app creada'
    window = Gui()
    window.setControl(control)
    window.show()
    print 'window'

    t1 = ThreadControl(control)  
    t1.start()
    print 'threadcontrol'
    
    t2 = ThreadGui(window)  
    t2.start()
    print 'threadgui'

    sys.exit(app.exec_())

