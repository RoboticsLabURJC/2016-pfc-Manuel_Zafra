# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
import numpy

class Gui(QtGui.QMainWindow):

    def __init__(self, control):
        self.control = control
        self.image = self.control.getImage()
        self.imageAux = None

        QtCore.QObject.connect(self, QtCore.SIGNAL('setPixmap()'),
                               self.setPixmap)

    def setPixmap(self):
        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(self.imageAux))

    def update(self):

        self.image = self.control.getImage()

+
        img = numpy.zeros((self.image.description.height *
                           self.image.description.width * 3),
                           dtype=numpy.uint8)

        img = numpy.frombuffer(self.image.pixelData, dtype=numpy.uint8)

        img.shape = (self.image.description.height,
                     self.image.description.width, 3)

        self.imageAux = QtGui.QImage(img.data, img.shape[1], img.shape[0],
                                img.shape[1] * img.shape[2],
                                QtGui.QImage.Format_RGB888)

        self.emit(QtCore.SIGNAL('setPixmap()'))
