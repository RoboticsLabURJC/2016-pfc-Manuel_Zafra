# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4.QtOpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt4 import QtCore, QtGui, QtOpenGL
import collada
import math
import sys
import pickle
import OBJFile


class Gui(QtGui.QWidget):

    def __init__(self):
        super(Gui, self).__init__()

        self.setWindowTitle('Drone Navigator')
        self.setMinimumSize(780,470)
        self.setMaximumSize(780,470)

        self.changeCam = QtGui.QPushButton("Change Camera")
        self.changeCam.setMinimumSize(250,40)
        self.changeCam.setMaximumSize(250,40)
        self.changeCam.setParent(self)
        self.changeCam.clicked.connect(self.changeCamera)

        self.changeView = QtGui.QPushButton("Change View")
        self.changeView.setMinimumSize(250,40)
        self.changeView.setMaximumSize(250,40)
        self.changeView.setParent(self)
        self.changeView.clicked.connect(self.changeViewpoint)

        self.posText = QtGui.QLabel(self)
        self.posText.setMinimumSize(250,100)
        self.posText.setMaximumSize(250,100)
        self.posText.show()

        self.glWidget = GLWidget()
        self.glWidget.setMinimumSize(450,450)
        self.glWidget.setMaximumSize(450,450)
        self.glWidget.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.imgLabel=QtGui.QLabel(self)
        self.imgLabel.setMinimumSize(250,250)
        self.imgLabel.setMaximumSize(250,250)
        self.imgLabel.show()
        self.connect(self, QtCore.SIGNAL("NewImg"), self.update_img)
        
        VLayout = QtGui.QVBoxLayout()
        VLayout.addStretch(1)
        VLayout.addWidget(self.imgLabel)
        VLayout.addStretch(1)
        VLayout.addWidget(self.changeCam)
        VLayout.addStretch(1)
        VLayout.addWidget(self.changeView)
        VLayout.addStretch(1)
        VLayout.addWidget(self.posText)
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

    def changeViewpoint(self):
        self.glWidget.toggleView()

    def update(self):
        pose3d = self.interface.getPose3D()
        self.glWidget.setPose3D(pose3d)
        route = self.interface.getRoute()
        self.glWidget.setRoute(route)
        self.glWidget.update()
        image = self.interface.getImage()
        if image != None:
            self.emit(QtCore.SIGNAL("NewImg"), image)
        self.posText.setText("Position: \n(%f, %f, %f)"
            %(pose3d.x, pose3d.y, pose3d.z))

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
        self.viewpoint = True
        self.view_d = 20.0
        self.view_ang = math.radians(60.0)
        self.eyex = self.view_d * math.sin(self.view_ang)
        self.eyey = 0.0
        self.eyez = abs(self.view_d * math.cos(self.view_ang))
        self.rot = 20.0 #degrees
        self.drone3d = OBJFile.OBJFile('gui/quadrotor/blender/quadrotor_CAD2.obj')

    def setPose3D(self, pose3d):
        self.pose3d = pose3d
        if self.pose3d != None :
            self.dX = pose3d.x
            self.dY = pose3d.y
            self.dZ = pose3d.z
            self.trailbuff.append(self.pose3d)

    def setRoute(self, pose3d):
        if pose3d != None :
            #self.routbuff.append(pose3d)
            self.routbuff = pose3d

    def initializeGL(self):
        glClearColor(0.2, 0.2, 0.2, 1);

        glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH) 

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective( 60, 1, 1, 1000 )
        glMatrixMode(GL_MODELVIEW)
        gluLookAt( self.eyex,self.eyey,self.eyez, 0,0,0, 0,0,1)
        glRotatef( self.rot, 0, 0, 1 )


    def paintGL(self):


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #glMatrixMode(GL_PROJECTION) # Select The Projection Matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        if self.viewpoint == True :
            gluLookAt( self.eyex,self.eyey,self.eyez, 0,0,0, 0,0,1)
            glRotatef( self.rot, 0, 0, 1 )
        else :
            gluLookAt( self.dX + self.view_d*math.cos(15) ,
                        self.dY + self.view_d*math.cos(15) ,
                        self.dZ + self.view_d*math.sin(15) ,
                        self.dX, self.dY, self.dZ,
                        0,0,1)
        self.axis()
        self.floor()
        self.trail()
        if self.routbuff != None :
            self.route()
        if self.pose3d != None :
            self.drone()
        self.swapBuffers()


    def axis(self):
        #Draws 3d axis
        glLineWidth(2)
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(5, 0, 0)
        glEnd()
        glColor3f(0.0, 1.0, 0.0)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 5, 0)
        glEnd()
        glColor3f(0.0, 0.0, 1.0)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 5)
        glEnd()

    def floor(self):
        #Draws floor grid
        glLineWidth(0.5)
        glColor3f(0.0, 0.0, 0.0)
        for x in range(-10,11):
            glBegin(GL_LINES)
            glVertex3f(x*2, -20, 0)
            glVertex3f(x*2, 20, 0)
            glEnd()
            glBegin(GL_LINES)
            glVertex3f(20, x*2, 0)
            glVertex3f(-20, x*2, 0)
            glEnd()

    def drone(self):
        #Draws drone position
        glDisable(GL_COLOR_MATERIAL)
        yaw = self.qtoyaw(self.pose3d.q0,self.pose3d.q1,self.pose3d.q2,self.pose3d.q3)
        glPushMatrix();
        glTranslate(self.dX,self.dY,self.dZ)
        glRotatef(yaw,0,0,1)
        self.drone3d.draw()
        glPopMatrix()
        glEnable(GL_COLOR_MATERIAL)

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
        glPointSize(2)
        (xx, yy, zz) = self.routbuff[0]

        for (x,y,z) in self.routbuff:
            glBegin(GL_POINTS)
            glVertex(x,y,z)
            glEnd()
            glBegin(GL_LINES)
            glVertex3f(x,y,z)
            glVertex3f(xx,yy,zz)
            glEnd()
            (xx, yy, zz) = (x, y, z)

    def drawTrailLine(self, poseA, poseB):
        #Draws line between two given pose3D data structures
        glBegin(GL_LINES)
        glVertex3f(poseA.x, poseA.y, poseA.z)
        glVertex3f(poseB.x, poseB.y, poseB.z)
        glEnd()

    def qtoyaw(self, q0,q1,q2,q3):
        #Transforms quaternions to (yaw,pitch,roll) 
        yaw = math.atan2(2.0*(q0*q3 + q1*2), 1 - 2*(q2*q2 + q3*q3));
        return math.degrees(yaw)  #[degrees]

    def toggleView(self):
        self.viewpoint = not self.viewpoint
        if not self.viewpoint : self.view_d = 5

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Right :
            self.rot -= 2
        elif e.key() == QtCore.Qt.Key_Left :
            self.rot += 2
	    #elif
        if e.key() == QtCore.Qt.Key_Up :
            self.view_ang -= math.radians(0.7)
            if self.view_ang > math.radians(90):
                self.view_ang = math.radians(90)
            self.eyex = self.view_d * math.sin(self.view_ang)
            self.eyez = abs(self.view_d * math.cos(self.view_ang))
        elif e.key() == QtCore.Qt.Key_Down :
            self.view_ang += math.radians(0.7)
            if self.view_ang < 0.0:
                self.view_ang = 0.0
            self.eyex = self.view_d * math.sin(self.view_ang)
            self.eyez = abs(self.view_d * math.cos(self.view_ang))

    def wheelEvent(self, e):
        if e.delta() > 0 :
            self.view_d -= 1
        elif e.delta() < 0 :
            self.view_d += 1
        self.eyex = self.view_d * math.sin(self.view_ang)
        self.eyez = abs(self.view_d * math.cos(self.view_ang))



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

