import sys, traceback, Ice
import jderobot
import numpy as np
import threading
import math

class Pilot():

    def __init__(self, interface):
        self.step = 0
        self.setVel(0.2,0.3)
        self.interface = interface
        self.path = self.interface.getPath(0)
        self.navState = 0
            # 0 = Start
            # 1 = Movement
            # 2 = Close to point
        self.startCount = 0


    def update(self):
        pose3d = self.interface.getPose3D()

        if self.distance(pose3d) < 0.1:
            self.step += 1

        #self.checkState(d)
        print 'STEP : %i' %self.step
        self.path = self.interface.getPath(self.step)

        self.pilot(pose3d)

    def pilot(self, pose3d):
        #Calculates drone's movement command

        """
        self.checkState(d)
    
        if self.navState = 0 :

        elif self.navState = 1 :

        elif self.navState = 2 :
        """


        d = self.distance(pose3d)

        (px,py,pz) = self.path

        ux = (px - pose3d.x) / d
        uy = (py - pose3d.y) / d
        uz = (pz - pose3d.z) / d

        if ux < 0.0001:
            ux = 0.0001

        alpha = math.degrees(math.atan(uy / ux))

        if px < pose3d.x:
            if py > pose3d.y:
                alpha = 180 + alpha
            else:
                alpha = (180 - alpha)*(-1)

        alpha = math.radians(alpha)
        yaw = self.qtoyaw(pose3d.q0,pose3d.q1,pose3d.q2,pose3d.q3)

        yaw_d = self.angularDirection(yaw, alpha)

        uy = uy * self.Vel
        ux = ux * self.Vel
        uz = uz * self.Vel
        uw = yaw_d * self.AngVel

        #print ' d = %f' %d
        #print ' Pz = %f' %pz        
        #print ' Px = %f' %px
        #print ' X = %f' %pose3d.x
        #print ' q0 = %f' %pose3d.q0
        #print ' q1 = %f' %pose3d.q1
        #print ' q2 = %f' %pose3d.q2
        #print ' q3 = %f' %pose3d.q3
        print ' Ux = %f' %ux
        print ' Uw = %f' %uw
        print ' Alpha = %f' %alpha
        print ' yaw = %f' %yaw
        print ' - - - - - - - - - - -'

        self.interface.sendCMDVel(0, 0, 0, 0.3)


    def setVel(self, v, w):
        self.Vel = v
        self.AngVel = w

    """
    def checkState(self, d):

        if d < 0.1:
            self.step += 1
            self.navState = 0
        else:
            

        if self.navState = 0 :#start
            if self.startCount < 10:
                self.startCount += 1
            else:
                self.navState = 1
        elif self.navState = 1 :#movement

        elif self.navState = 2 :#closetopoint
    """



    def angularDirection(self, yaw, alpha):
        #Calculates angular direction
        #Clockwise = (-1)
        #Anticlockwise = 1
        yaw_d = 0
        if (((alpha >= 0) and (yaw >= 0)) or ((alpha < 0) and (yaw < 0))):
        # alpha+ yaw+ | alpha- yaw-
            if alpha > yaw :
                yaw_d = 1   #turn left
            else:
                yaw_d = -1  #turn right
        else:
            if (alpha < 0):
            #alpha- yaw+
                if ((math.pi - abs(alpha)) > yaw) :
                    yaw_d = 1   #turn left
                else:
                    yaw_d = -1  #turn right
            else:
            #alpha+ yaw-
                if ((math.pi - abs(yaw)) > alpha) :
                    yaw_d = 1  #turn right
                else:
                    yaw_d = -1   #turn left
        return yaw_d

    def qtoyaw(self, q0,q1,q2,q3):
        #Transforms quaternions to (yaw,pitch,roll)
        yaw = math.atan2(2.0*(q0*q3 + q1*2), 1 - 2*(q2*q2 + q3*q3));
        return yaw  #[-pi,pi]

    def distance(self, pose3d):
        #Distance between drone position and next point
        (a,b,c) = self.path
        d = math.sqrt((pose3d.x - a)**2 + (pose3d.y - b)**2)# + (pose3d.z - c)**2)
        return d
