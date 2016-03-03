# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4.QtOpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt4 import QtCore, QtGui, QtOpenGL
import math
import sys
import pickle


class Gui(QtGui.QWidget):

    def __init__(self):
        super(Gui, self).__init__()

        self.setWindowTitle('Drone Navigator')
        self.setMinimumSize(730,420)
        self.setMaximumSize(730,420)

        changeCam = QtGui.QPushButton("Change Camera")
        changeCam.setMinimumSize(250,40)
        changeCam.setMaximumSize(250,40)
        changeCam.setParent(self)
        changeCam.clicked.connect(self.changeCamera)

        self.glWidget = GLWidget()
        self.glWidget.setMinimumSize(400,400)
        self.glWidget.setMaximumSize(400,400)

        self.imgLabel=QtGui.QLabel(self)
        self.imgLabel.setMinimumSize(250,250)
        self.imgLabel.setMaximumSize(250,250)
        self.imgLabel.show()
        self.connect(self, QtCore.SIGNAL("NewImg"), self.update_img)
        
        VLayout = QtGui.QVBoxLayout()
        VLayout.addStretch(1)
        VLayout.addWidget(self.imgLabel)
        VLayout.addStretch(1)
        VLayout.addWidget(changeCam)
        VLayout.addStretch(1)

        HLayout = QtGui.QHBoxLayout()
        HLayout.addStretch(1)
        HLayout.addLayout(VLayout)
        HLayout.addStretch(1)
        HLayout.addWidget(self.glWidget)
        HLayout.addStretch(1)

        self.setLayout(HLayout)
        

    def setInterface(self,interface):
        self.interface=interface

    def changeCamera(self):
        self.interface.toggleCam()

    def update(self):
        pose3d = self.interface.getPose3D()
        self.glWidget.setPose3D(pose3d)
        route = self.interface.getRoute()
        self.glWidget.setRoute(route)
        self.glWidget.update()
        image = self.interface.getImage()
        if image != None:
            self.emit(QtCore.SIGNAL("NewImg"), image)

    def update_img(self, image):
        img = QtGui.QImage(image.data, image.shape[1], image.shape[0], QtGui.QImage.Format_RGB888)
        #size=QtCore.QSize(image.shape[1],image.shape[0])
        #self.imgLabel.resize(size)
        self.imgLabel.setPixmap(QtGui.QPixmap.fromImage(img))




# OPENGL WIDGET CLASS

class GLWidget(QtOpenGL.QGLWidget):

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.pose3d = None
        self.trailbuff = RingBuffer(150)
        #self.routbuff = RingBuffer(250)
        self.routbuff = []

    def setPose3D(self, pose3d):
        self.pose3d = pose3d
        if self.pose3d != None :
            self.dX = 2*pose3d.x
            self.dY = 2*pose3d.y
            self.dZ = 2*pose3d.z
            self.trailbuff.append(self.pose3d)

    def setRoute(self, pose3d):
        if pose3d != None :
            #self.routbuff.append(pose3d)
            self.routbuff = pose3d

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.axis()
        self.floor()
        if self.pose3d != None :
            self.drone()
        self.trail()
        if self.routbuff != None :
            self.route()
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
        #Draws drone position
        yaw = self.qtoyaw(self.pose3d.q0,self.pose3d.q1,self.pose3d.q2,self.pose3d.q3)
        glPushMatrix();
        glTranslate(self.dX,self.dY,self.dZ)
        glRotatef(yaw,0,0,1)
        glColor3f(0.9, 0.9, 0.9)
        c = gluNewQuadric()
        gluCylinder(c,1.3,1.3,0.7,6,4)
        glPointSize(4)
        glBegin(GL_POINTS)
        glVertex(0,0,0)
        glEnd()
        glColor3f(0.9, 0.2, 0.2)
        glLineWidth(2.5)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0.3)
        glVertex3f(2, 0, 0.3)
        glEnd()
        glPopMatrix();

    def trail(self):
        #Draws drone's movement trail
        glLineWidth(1)
        glColor3f(0.2, 0.5, 0.2)
        for x in range(1,self.trailbuff.getlen()-1):
            self.drawTrailLine(self.trailbuff.get(x),self.trailbuff.get(x+1))

    def route(self):
        #Draws drone's path
        #glLineWidth(1)
        #glColor3f(0.7, 0.3, 0.3)
        #for x in range(1,self.routbuff.getlen()-1):
        #    self.drawTrailLine(self.routbuff.get(x),self.routbuff.get(x+1))
        glColor3f(0.7, 0.3, 0.3)
        glPointSize(4)
        (xx, yy, zz) = self.routbuff[0]

        for (x,y,z) in self.routbuff:
            glBegin(GL_POINTS)
            glVertex(x*2,y*2,z*2)
            glEnd()
            glBegin(GL_LINES)
            glVertex3f(x*2,y*2,z*2)
            glVertex3f(xx*2,yy*2,zz*2)
            glEnd()
            (xx, yy, zz) = (x, y, z)

    def drawTrailLine(self, poseA, poseB):
        #Draws line between two given pose3D data structures
        glBegin(GL_LINES)
        glVertex3f(poseA.x*2, poseA.y*2, poseA.z*2)
        glVertex3f(poseB.x*2, poseB.y*2, poseB.z*2)
        glEnd()

    def qtoyaw(self, q0,q1,q2,q3):
        #Transforms quaternions to (yaw,pitch,roll)
        yaw = math.atan2(2.0*(q0*q3 + q1*2), 1 - 2*(q2*q2 + q3*q3));
        return math.degrees(yaw)  #[degrees]



class RingBuffer:
    #Class that implements a not-yet-full buffer
    def __init__(self,size_max):
        self.max = size_max
        self.data = []

    class __Full:
        #Class that implements a full buffer
        def append(self, x):
            self.data[self.cur] = x
            self.cur = (self.cur+1) % self.max
        def get(self,x):
            return self.data[(self.cur+x) % self.max]
        def getlen(self):
            return self.max

    def append(self,x):
        self.data.append(x)
        if len(self.data) == self.max:
            self.cur = 0
            # Permanently change self's class from non-full to full
            self.__class__ = self.__Full

    def get(self,x):
        #Return data in the given position
        return self.data[x]

    def getlen(self):
        return len(self.data)

