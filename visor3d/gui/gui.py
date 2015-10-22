# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
import numpy
import sys

class Gui(QtGui.QWidget):

    updGUI=QtCore.pyqtSignal()
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle("Visor3D")
        self.imgLabel=QtGui.QLabel(self)
        self.imgLabel.show()
        size=QtCore.QSize(350,350)
        self.imgLabel.resize(size)
        self.resize(size)
        self.updGUI.connect(self.update)

    def setControl(self,control):
        self.control=control

    def update(self):
        print 'updgui'
        image = self.control.getImage()
        if image != None:
            img = QtGui.QImage(image.data, image.shape[1], image.shape[0], QtGui.QImage.Format_RGB888)
            self.imgLabel.setPixmap(QtGui.QPixmap.fromImage(img))
            print 'printimg'

