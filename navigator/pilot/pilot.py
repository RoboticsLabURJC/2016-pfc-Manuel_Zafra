import sys, traceback, Ice
import jderobot
import numpy as np
import threading
import math

class Pilot():

    def __init__(self, interface):
        self.step = 0
        self.angDiff = 0
        self.pathError = 0
        self.posError = 0
        self.setVel(0.3,0.3)
        self.interface = interface
        self.path = self.interface.getPath(0)
        self.fullpath = self.loadpath()
        self.navState = 0
            # 0 = Start
            # 1 = Movement
            # 2 = Close to point
        self.startCount = 0


    def loadpath(self):
        a = []
        pose = jderobot.Pose3DData()
        pathfile = open('path.txt','r')
        for line in pathfile.readlines():
            line = line.rstrip('\n')
            linelist = line.split()
            pose.x = float(linelist[0])
            pose.y = float(linelist[1])
            pose.z = float(linelist[2])
            a.append(pose)
        pathfile.close()
        return np.array(a)



    def update(self):
        pose3d = self.interface.getRealPose3D()
        self.path = self.interface.getPath(self.step)
        self.pilot(pose3d)

    def pilot(self, pose3d):
        #Calculates drone's movement command

        d = self.distance(pose3d)

        (px,py,pz) = self.path

        ux = (px - pose3d.x) / d
        uy = (py - pose3d.y) / d
        uz = (pz - pose3d.z) / d

        alpha = math.degrees(math.atan(uy / ux))

        if px < pose3d.x:
            if py > pose3d.y:
                alpha = 90 + alpha #180
            else:
                alpha = (180 - alpha)*(-1)

        alpha = math.radians(alpha)
        yaw = self.qtoyaw(pose3d.q0,pose3d.q1,pose3d.q2,pose3d.q3)

        yaw_d = self.angularDirection(yaw, alpha)

        
        if self.navState == 0:
            #0.2 = 11degrees
            if self.angDiff >= 0.2 :
                self.setVel(0.1, 0.5)
            else: #self.angDiff < 0.2
                self.setVel(0.2, 0.3)
                self.navState = 1
            ux = abs(ux)
            ux += abs(uy)
            uy = 0.0

        elif self.navState == 1:
            if d >= 0.3 :
                ux = abs(ux)
                ux += abs(uy)
                uy = 0.0
                if self.angDiff <= 0.05 :
                    self.setVel(0.2, 0.01)
                else:
                    self.setVel(0.2, 0.2)
            else:
                self.setVel(0.15, 0.0)
                self.navState = 2

        elif self.navState == 2:
            ux = abs(ux)
            ux += abs(uy)
            uy = 0.0
            if self.angDiff <= 0.05 :
                self.setVel(0.2, 0.01)
            else:
                self.setVel(0.2, 0.2)

            if d < 0.1:
                self.step += 1
                self.navState = 0
        """
            if d < 0.1:
                self.step += 1
                self.navState = 0
                self.setVel(0.1, 0.0)
            else:
                self.setVel(0.1, 0.0)
            yaw_d = 0.0
        """

        #######
        self.Vel = 0.1
        #######

        uy = uy * self.Vel
        ux = ux * self.Vel
        uz = uz * self.Vel
        uw = yaw_d * self.AngVel



        self.interface.sendCMDVel(ux, uy, uz, uw)
        #self.interface.sendCMDVel(0, 0, 0, 0)

        print 'STEP : %i' %self.step
        print 'State : %i' %self.navState
        print ' d = %f' %d
        #print ' Pz = %f' %pz        
        #print ' Px = %f' %px
        #print ' X = %f' %pose3d.x
        print ' U(x,y,z) = (%f, %f, %f)' %(ux, uy, uz)
        print ' Uw = %f' %uw
        #print ' Alpha = %f' %alpha
        #print ' yaw = %f' %yaw
        print ' - - - - - - - - - - -'

    def setVel(self, v, w):
        self.Vel = v
        self.AngVel = w

    def setAngVel(self, w):
        self.AngVel = w

    def setLinVel(self, v):
        self.Vel = v

    def angularDirection(self, yaw, alpha):
        #Calculates angular direction
        #Clockwise = 1
        #Anticlockwise = -1
        yaw_d = 0
        if (((alpha >= 0.0) and (yaw >= 0.0)) or ((alpha < 0.0) and (yaw < 0.0))):
        # alpha+ yaw+ | alpha- yaw-
            if alpha > yaw :
                yaw_d = 1   #turn left
                self.angDiff = alpha - yaw
            else:
                yaw_d = -1  #turn right
                self.angDiff = yaw - alpha
        else:
            if (alpha < 0.0):
            #alpha- yaw+
                if ((math.pi - abs(alpha)) > yaw) :
                    self.angDiff = abs(alpha) + yaw
                    yaw_d = -1   #turn left
                else:
                    self.angDiff = 2*math.pi + alpha - yaw
                    yaw_d = 1  #turn right
            else:
            #alpha+ yaw-
                if ((math.pi - abs(yaw)) > alpha) :
                    self.angDiff = abs(yaw) + alpha
                    yaw_d = 1  #turn left
                else:
                    self.angDiff = 2*math.pi + yaw - alpha
                    yaw_d = -1   #turn right
        return yaw_d

    def qtoyaw(self, q0,q1,q2,q3):
        #Transforms quaternions to (yaw,pitch,roll)
        yaw = math.atan2(2.0*(q0*q3 + q1*2), 1 - 2*(q2*q2 + q3*q3));
        return yaw  #[-pi,pi]

    def distance(self, pose3d):
        #Distance between drone position and next point
        (a,b,c) = self.path
        d = math.sqrt((pose3d.x - a)**2 + (pose3d.y - b)**2 + (pose3d.z - c)**2)
        return d

    def poseError(self, pose3d1, pose3d2):
        d = math.sqrt((pose3d1.x - pose3d2.x)**2 + (pose3d1.x - pose3d2.x)**2 + (pose3d1.x - pose3d2.x)**2)
        return d
