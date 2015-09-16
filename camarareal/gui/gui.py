# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
import numpy
import sys

class Gui(QtGui.QWidget):

    updGUI=QtCore.pyqtSignal()
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle("CamaraReal")
        self.imgLabel=QtGui.QLabel(self)
        self.imgLabel.show()
        self.updGUI.connect(self.update)

        TestButton=QtGui.QPushButton("Test")
        TestButton.resize(40,40)
        TestButton.setParent(self)
        TestButton.clicked.connect(self.effect)

    def setControl(self,control):
        self.control=control

    def update(self):
        print 'updgui'
        image = self.control.getImage()
        if image != None:
            img = QtGui.QImage(image.data, image.shape[1], image.shape[0], QtGui.QImage.Format_RGB888)
            size=QtCore.QSize(image.shape[1],image.shape[0])
            self.imgLabel.resize(size)
            self.resize(size)
            self.imgLabel.setPixmap(QtGui.QPixmap.fromImage(img))
            print 'printimg'

    def effect(self):
        self.control.effect()

