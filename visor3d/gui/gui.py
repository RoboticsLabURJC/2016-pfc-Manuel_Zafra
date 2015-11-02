# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4.QtOpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt4 import QtCore, QtGui, QtOpenGL
import math
import sys


class Gui(QtGui.QWidget):

    def __init__(self):
        super(Gui, self).__init__()

        self.glWidget = GLWidget()
        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addWidget(self.glWidget)
        self.setLayout(mainLayout)
        self.setWindowTitle("Visor3D")
        self.resize(550,400)

    def setControl(self,control):
        self.control=control

    def update(self):
        pose3d = self.control.getPose3D()
        self.glWidget.setPose3D(pose3d)
        self.glWidget.update()
        print 'updgui'

class GLWidget(QtOpenGL.QGLWidget):

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.pose3d = None

    def setPose3D(self, pose3d):
        self.pose3d = pose3d
        if self.pose3d != None :
            self.dX = 2*pose3d.x
            self.dY = 2*pose3d.y
            self.dZ = 2*pose3d.z

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.axis()
        self.floor()
        if self.pose3d != None :
            self.drone()
        self.swapBuffers()

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 0.0);
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def resizeGL(self, w, h):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective( 60, 1, 1, 1000 )
        glMatrixMode( GL_MODELVIEW )
        gluLookAt( 30,30,40, 0,0,5, 0,0,1)
        glRotatef( 20, 0, 0, 1 )

    def axis(self):
        #Draws 3d axis
        glLineWidth(2)
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(10, 0, 0)
        glEnd()
        glColor3f(0.0, 1.0, 0.0)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 10, 0)
        glEnd()
        glColor3f(0.0, 0.0, 1.0)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 10)
        glEnd()

    def floor(self):
        #Draws floor grid
        glLineWidth(1)
        glColor3f(0.2, 0.2, 0.2)
        for x in range(-10,11):
            glBegin(GL_LINES)
            glVertex3f(x*3, -30, 0)
            glVertex3f(x*3, 30, 0)
            glEnd()
            glBegin(GL_LINES)
            glVertex3f(30, x*3, 0)
            glVertex3f(-30, x*3, 0)
            glEnd()

    def drone(self):
        glPushMatrix();
        glTranslate(self.dX,self.dY,self.dZ)
        glColor3f(0.9, 0.9, 0.9)
        c = gluNewQuadric()
        gluCylinder(c,1.3,1.3,0.7,6,4)
        glPointSize(4)
        glBegin(GL_POINTS)
        glVertex(0,0,0)
        glEnd()
        glPopMatrix();

