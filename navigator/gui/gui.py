# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from PyQt4 import QtGui
from PyQt4.QtOpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt4 import QtCore, QtGui, QtOpenGL
from collada import *
from .OBJFile import OBJFile
import math
import jderobot
import numpy as np
import sys
import pyqtgraph as pg


class Gui(QtGui.QWidget):

    def __init__(self):
        super(Gui, self).__init__()

        self.setWindowTitle('Drone Navigator')
        self.setMinimumSize(750,800)
        self.setMaximumSize(750,800)

        self.startButton = QtGui.QPushButton("Start")
        self.startButton.setMinimumSize(250,38)
        self.startButton.setMaximumSize(250,38)
        self.startButton.setParent(self)
        self.startButton.clicked.connect(self.startdrone)

        self.pauseButton = QtGui.QPushButton("Pause")
        self.pauseButton.setMinimumSize(250,38)
        self.pauseButton.setMaximumSize(250,38)
        self.pauseButton.setParent(self)
        self.pauseButton.clicked.connect(self.pausedrone)

        self.landButton = QtGui.QPushButton("Land")
        self.landButton.setMinimumSize(120,38)
        self.landButton.setMaximumSize(120,38)
        self.landButton.setParent(self)
        self.landButton.clicked.connect(self.landdrone)

        self.takeoffButton = QtGui.QPushButton("Take Off")
        self.takeoffButton.setMinimumSize(120,38)
        self.takeoffButton.setMaximumSize(120,38)
        self.takeoffButton.setParent(self)
        self.takeoffButton.clicked.connect(self.takeoffdrone)

        self.changeView = QtGui.QPushButton("Change View")
        self.changeView.setMinimumSize(120,38)
        self.changeView.setMaximumSize(120,38)
        self.changeView.setParent(self)
        self.changeView.clicked.connect(self.changeViewpoint)

        self.toggleCam = QtGui.QPushButton("Toggle Cam")
        self.toggleCam.setMinimumSize(120,38)
        self.toggleCam.setMaximumSize(120,38)
        self.toggleCam.setParent(self)
        self.toggleCam.clicked.connect(self.togglecam)

        self.glWidget = GLWidget()
        self.glWidget.setMinimumSize(450,450)
        self.glWidget.setMaximumSize(450,450)
        self.glWidget.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.imgLabel=QtGui.QLabel(self)
        self.imgLabel.setMinimumSize(250,250)
        self.imgLabel.setMaximumSize(250,250)
        self.imgLabel.show()

        self.plotWidget = pg.GraphicsWindow()
        pg.setConfigOptions(antialias=True)
        self.plotWidget.setMinimumSize(720,300)
        self.plotWidget.setMaximumSize(720,300)

        self.poseErrorplot = self.plotWidget.addPlot()
        self.poseErrorplot.showAxis('bottom', False)
        self.poseErrorplot.setRange(yRange=[0,3])
        self.poseErrorplot.showGrid(y=True)
        self.poseErrordata =np.zeros(250) 
        self.poseErrorplot.addLegend()
        self.poseErrorcurve = self.poseErrorplot.plot(self.poseErrordata, pen=(255,0,0),
            name="Pose3D Error")
        self.angleErrordata =np.zeros(250) 
        self.angleErrorplot = self.plotWidget.addPlot()
        self.angleErrorplot.showAxis('bottom', False)
        self.angleErrorplot.setRange(yRange=[0,180])
        self.angleErrorplot.showGrid(y=True)
        self.angleErrorplot.addLegend()
        self.angleErrorcurve = self.angleErrorplot.plot(self.angleErrordata, pen=(0,255,0),
            name="Angle Error")

        self.ptr = 0      
        self.connect(self, QtCore.SIGNAL("NewImg"), self.update_img)

        HButtonLayout1 = QtGui.QHBoxLayout()
        HButtonLayout1.addStretch(1)
        HButtonLayout1.addWidget(self.takeoffButton)
        HButtonLayout1.addStretch(1)
        HButtonLayout1.addWidget(self.landButton)
        HButtonLayout1.addStretch(1)

        HButtonLayout2 = QtGui.QHBoxLayout()
        HButtonLayout2.addStretch(1)
        HButtonLayout2.addWidget(self.changeView)
        HButtonLayout2.addStretch(1)
        HButtonLayout2.addWidget(self.toggleCam)
        HButtonLayout2.addStretch(1)

        VLayoutButtons = QtGui.QVBoxLayout()
        VLayoutButtons.addStretch(1)
        VLayoutButtons.addWidget(self.startButton)
        VLayoutButtons.addStretch(1)
        VLayoutButtons.addWidget(self.pauseButton)
        VLayoutButtons.addStretch(1)
        VLayoutButtons.addLayout(HButtonLayout1)
        VLayoutButtons.addStretch(1)
        VLayoutButtons.addLayout(HButtonLayout2)
        VLayoutButtons.addStretch(1)


        VLayout = QtGui.QVBoxLayout()
        VLayout.addStretch(1)
        VLayout.addWidget(self.imgLabel)
        VLayout.addStretch(1)
        VLayout.addLayout(VLayoutButtons)
        VLayout.addStretch(1)

        HLayout = QtGui.QHBoxLayout()
        HLayout.addStretch(1)
        HLayout.addLayout(VLayout)
        HLayout.addStretch(1)
        HLayout.addWidget(self.glWidget)
        HLayout.addStretch(1)

        MainLayout = QtGui.QVBoxLayout()
        MainLayout.addStretch(1)
        MainLayout.addLayout(HLayout)
        MainLayout.addStretch(1)
        MainLayout.addWidget(self.plotWidget)
        MainLayout.addStretch(1)

        self.setLayout(MainLayout)
        

    def setInterface(self,interface):
        self.interface=interface

    def pausedrone(self):
        self.interface.pausedrone()

    def landdrone(self):
        self.interface.landdrone()

    def startdrone(self):
        self.interface.startdrone()

    def changeViewpoint(self):
        self.glWidget.toggleView()

    def takeoffdrone(self):
        self.interface.takeoffdrone()

    def togglecam(self):
        self.interface.togglecam()

    def update(self):
        pose3d = self.interface.getPose3D()
        self.glWidget.setPose3D(pose3d)
        realpose3d = self.interface.getRealPose3D()
        self.glWidget.setRealPose3D(realpose3d)
        self.glWidget.update()
        image = self.interface.getImage()
        #self.posText.setText("Position: \n(%f, %f, %f)"
        #    %(pose3d.x, pose3d.y, pose3d.z))
        if self.ptr == 249 :
            self.poseErrordata = np.roll(self.poseErrordata, -1)
            self.angleErrordata = np.roll(self.angleErrordata, -1)
        else : self.ptr += 1
        self.poseErrordata[self.ptr] = self.poseError(realpose3d, pose3d)
        self.angleErrordata[self.ptr] = self.angleError(realpose3d, pose3d)
        if image != None:
            self.emit(QtCore.SIGNAL("NewImg"), image)

    def update_img(self, image):
        img = QtGui.QImage(image.data, image.shape[1], image.shape[0], QtGui.QImage.Format_RGB888)
        #size=QtCore.QSize(image.shape[1],image.shape[0])
        #self.imgLabel.resize(size)
        self.imgLabel.setPixmap(QtGui.QPixmap.fromImage(img))
        self.poseErrorcurve.setData(self.poseErrordata)
        self.angleErrorcurve.setData(self.angleErrordata)

    def poseError(self, pose3d1, pose3d2):
        d = math.sqrt((pose3d1.x - pose3d2.x)**2 + (pose3d1.x - pose3d2.x)**2 + (pose3d1.x - pose3d2.x)**2)
        return d
        
    def angleError(self, pose3d1, pose3d2):
        (r1,p1,y1) = self.qtorpy(pose3d1)
        (r2,p2,y2) = self.qtorpy(pose3d2)

        e = math.sqrt((self.angleDiff(r1,r2))**2 + (self.angleDiff(p1,p2))**2 + (self.angleDiff(y1,y2))**2)
        if (e > math.pi) :
            e = 2*math.pi - e
        return math.degrees(e)

    def angleDiff(self, a1, a2):
        angDifference = a1 - a2
        while (angDifference < -math.pi):
            angDifference = angDifference + 2*math.pi
        while (angDifference > math.pi):
            angDifference = angDifference - 2*math.pi
        return angDifference

    def qtorpy(self, pose):
        #Transforms quaternions to (roll,pitch,yaw) 
        roll = math.atan2(2*(pose.q0*pose.q1 + pose.q2*pose.q3), 1 - 2*(pose.q1**2 + pose.q2**2))
        pitch = math.asin(2*(pose.q0*pose.q2 - pose.q3*pose.q1))
        yaw = math.atan2(2.0*(pose.q0*pose.q3 + pose.q1*2), 1 - 2*(pose.q2*pose.q2 + pose.q3*pose.q3))
        return (roll,pitch,yaw)  #[degrees]


# OPENGL WIDGET CLASS

class GLWidget(QtOpenGL.QGLWidget):

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.pose3d = None
        self.realpose3d = None
        self.trailbuff = RingBuffer(250)
        self.realtrailbuff = RingBuffer(150)
        self.path = []
        self.loadpath()
        self.viewpoint = True
        self.view_d = 20.0
        self.view_ang = math.radians(60.0)
        self.eyex = self.view_d * math.sin(self.view_ang)
        self.eyey = 0.0
        self.eyez = abs(self.view_d * math.cos(self.view_ang))
        self.rot = 20.0 #degrees
        self.drone3d = OBJFile('gui/quadrotor/blender/quadrotor_CAD2.obj')

    def loadpath(self):
        a = []
        for line in open('path.txt','r').readlines():
            pose = jderobot.Pose3DData()
            line = line.rstrip('\n')
            linelist = line.split()
            #print linelist[0]
            pose.x = float(linelist[0])
            pose.y = float(linelist[1])
            pose.z = float(linelist[2])
            a.append(pose)
        #print 'pintando ruta?? %f' %a[5].x
        self.path = list(a)
        #print 'pintando ruta?? %f' %self.path[5].x

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
        self.realtrail()
        self.route()
        if self.pose3d != None :
            self.drone()
        self.swapBuffers()
        #print '%f' %self.path[0].x

    def setPose3D(self, pose3d):
        self.pose3d = pose3d
        if self.pose3d != None :
            self.trailbuff.append(self.pose3d)
        

    def setRealPose3D(self, pose3d):
        self.realpose3d = pose3d
        if self.realpose3d != None :
            self.dX = pose3d.x
            self.dY = pose3d.y
            self.dZ = pose3d.z
            self.realtrailbuff.append(self.realpose3d)

    def initializeGL(self):
        glClearColor(0.6, 0.6, 0.6, 1);

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


    def axis(self):
        #Draws 3d axis
        glLineWidth(2)
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0.001)
        glVertex3f(5, 0, 0.001)
        glEnd()
        glColor3f(0.0, 1.0, 0.0)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0.001)
        glVertex3f(0, 5, 0.001)
        glEnd()
        glColor3f(0.0, 0.0, 1.0)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0.001)
        glVertex3f(0, 0, 5.001)
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
        yaw = self.qtoyaw(self.realpose3d.q0,self.realpose3d.q1,
            self.realpose3d.q2,self.realpose3d.q3)
        glPushMatrix();
        glTranslate(self.dX,self.dY,self.dZ)
        glRotatef(yaw,0,0,1)
        self.drone3d.draw()
        glPopMatrix()
        glEnable(GL_COLOR_MATERIAL)

    def trail(self):
        #Draws drone's movement trail
        glLineWidth(2)
        glColor3f(0.2, 0.5, 0.2)
        for x in range(1,self.trailbuff.getlen()-1):
            self.drawTrailLine(self.trailbuff.get(x),self.trailbuff.get(x+1))

    def realtrail(self):
        #Draws drone's movement trail
        glLineWidth(2)
        glColor3f(0.15, 0.15, 0.5)
        for x in range(1,self.realtrailbuff.getlen()-1):
            self.drawTrailLine(self.realtrailbuff.get(x),self.realtrailbuff.get(x+1))

    def route(self):
        glLineWidth(2)
        glColor3f(0.7, 0.3, 0.3)
        glPointSize(3)
        glLineWidth(1)
        for pose0, pose1 in zip(self.path, self.path[1:]) :
            glBegin(GL_POINTS)
            glVertex(pose0.x,pose0.y,pose0.z)
            glEnd()
            glBegin(GL_LINES)
            #print 'pintando ruta?? %f' %pose1.x
            glVertex3f(pose1.x,pose1.y,pose1.z)
            glVertex3f(pose0.x,pose0.y,pose0.z)
            glEnd()
            #print pose.x

    def drawTrailLine(self, poseA, poseB):
        #Draws line between two given pose3D data structures
        glBegin(GL_LINES)
        glVertex3f(poseA.x, poseA.y, poseA.z)
        glVertex3f(poseB.x, poseB.y, poseB.z)
        glEnd()

    def qtoyaw(self, q0,q1,q2,q3):
        #Transforms quaternions to yaw
        yaw = math.atan2(2.0*(q0*q3 + q1*2), 1 - 2*(q2**2 + q3**2))
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


