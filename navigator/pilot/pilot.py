#!/usr/bin/env python3
import sys, traceback, Ice
import jderobot
import numpy as np
import threading
import math
from pilot.kalman import Kalman
from scipy.signal import savgol_filter as sgfilter

class Pilot():

    def __init__(self, interface, opt):
        """
        self.path = np.array([(-5.16,-1.92,1.38),(-4.28,-0.61,1.38),(-3.3,-0.61,1.38),
                (-2.72,-2.72,1.38),(-2.52,-3.74,1.58),(-2.52,-5.44,1.58),
                (-1.59,-6.87,1.22),(-1.14,-5.9,1.45),(-2.52,-5.04,1.52)])
                #(-2.52,-2.34,1.51),(-0.75,-2.34,1.51)]
        """
        self.step = 0
        self.angDiff = 0
        self.pathError = 0
        self.posError = 0
        #self.setVel(0.3,0.3)
        self.interface = interface
        self.loadpath(opt)
        self.Vel = 0.2 #0.03
        self.startCount = 0
        self.K1 = 0.01 #yaw adjustment gain rate
        self.tYaw = 0.0 #yaw control in t = t-1
        self.yawOffset = 0.2 #yaw offset limit
        self.K2 = 0.05 #yaw adjustment for spike detection
        self.tpose = jderobot.Pose3DData() #pose in t = t-1
        self.kalman = Kalman()
        self.yawFilterArray = np.zeros(5,float)


    def loadpath(self, opt):
        a = []
        filename = 'path.txt'
        if opt == 'sim' :
            filename = 'pathsim.txt'
        for line in open(filename,'r').readlines():
            pose = jderobot.Pose3DData()
            line = line.rstrip('\n')
            linelist = line.split()
            pose.x = float(linelist[0])
            pose.y = float(linelist[1])
            pose.z = float(linelist[2])
            #pose.q0 = float(linelist[3]) #roll
            #pose.q1 = float(linelist[4]) #pitch
            #pose.q2 = float(linelist[5]) #yaw
            #Uso cuaterniones anque en realidad hay angulos de euler
            a.append(pose)
        self.path = list(a)
        self.pathlen = len(self.path)



    def update(self):
        #pose3d = self.interface.getPose3D()
        pose3d = self.interface.getPose3D()
        self.pilot(pose3d)

    def pilot(self, pose3d):

        print (pose3d.x,pose3d.y,pose3d.z)

        #yaw = self.qtoyaw(pose3d.q0,pose3d.q1,pose3d.q2,pose3d.q3)
        yaw =  pose3d.q3
        
        jump = True #ver si el salto se produce a error en estimación(true)
                     #o a nuevo punto de ruta(false)

        #print ("Pose:")
        #print (pose3d.x, pose3d.y, pose3d.z)

        print (self.Vel)

        #HAY QUE CORREGIR YAW DE AUTOLOC
        yaw += (math.pi / 2)
        while (yaw < -math.pi):
            yaw += 2*math.pi
        while (yaw > math.pi):
            yaw -= 2*math.pi

        while(self.distance(pose3d, self.path[self.step]) < 0.35):
            self.step = self.step+1
            #self.step = 0  ###1pt
            jump = False #hemos avanzado en la ruta
            if self.step == self.pathlen :
                self.step = 0
        print ("STEP %f" %self.step)
        
        distance = self.distance(pose3d, self.path[self.step])
        self.interface.setPatherror(distance)

        '''
        if (((distance - self.tdistance) > 0.1) and jump ):
            #si ha habido salto en estimación de más de 0.4
            self.step += 1
            print("JUMP")
            #pasamos al siguiente punto

        self.tdistance = distance
        '''

        p = self.path[self.step]
        #Cálculo de vector al punto
        Vx = p.x - pose3d.x
        Vy = p.y - pose3d.y
        Vz = p.z - pose3d.z
        #Cálculo del vector unitario
        module = self.module(Vx, Vy, Vz)
        ux = Vx/module
        uy = Vy/module
        uz = Vz/module #Componente unitaria velocidad Vz
        uxy = math.sqrt(ux**2 + uy**2) #Componente unitaria velocidad Vx

        xVel = uxy * self.Vel
        zVel = uz * self.Vel

        #Error calculation
        #rx = self.path[self.step + 1].x - p.x
        #ry = self.path[self.step + 1].y - p.y

        ###CALCULARYAWAPELO###  
        ANGYAW = math.atan2(Vy, Vx)

        #print (ANGYAW, yaw)
        ANGe = ANGYAW - yaw
        while (ANGe < -math.pi):
            ANGe += 2*math.pi
        while (ANGe > math.pi):
            ANGe -= 2*math.pi


        #Position prediction
        L = xVel * 0.08 #L= travelled distance in an iteration
        Xf = L * math.cos(yaw) + pose3d.x
        Yf = L * math.sin(yaw) + pose3d.y


        #ANGe *= 0.8

        #Control law
        LatError = - math.sin(yaw)*(p.x-Xf) + math.cos(yaw)*(p.y-Yf)
        yawgain = (self.K1 * (LatError / xVel))

        Hdistance = math.sqrt(Vx**2 + Vy**2) #distancia horizontal
        deltae = ANGe / (Hdistance / xVel)
        yawcontrol = deltae + yawgain

        print ('ange , deltae, yawgain, final')
        print (ANGe, deltae, yawgain, yawcontrol)


        ########
        #yawcontrol = ANGe
        ########

        ####CONTROL DE VELOCIDAD SEGÚN ERROR LATERAL
        '''
        if math.fabs(LatError) > 0.5 :
            self.Vel = 0.02
        elif math.fabs(LatError) > 0.1 :
            self.Vel = 0.05
        else :
            self.Vel = 0.06
        '''


        #WEIGHTED-AVERAGE FILTER
        self.yawFilterArray = np.roll(self.yawFilterArray,1)
        self.yawFilterArray[0] = yawcontrol
        #print (self.yawFilterArray)
        yawcontrol = self.YawTemporalFilter()
        self.yawFilterArray[0] = yawcontrol

       # print (yawcontrol)
        
        """
        uy = uy * self.Vel
        ux = ux * self.Vel
        uz = uz * self.Vel
        uw = yaw_d * self.AngVel
        """

        
        #print (self.step)

        '''
        if math.fabs(xVel) > 0.2 :
            xVel = 0.2 * np.sign(xVel)
        if math.fabs(zVel) > 0.3 :
            zVel = 0.3 * np.sign(zVel)
        if math.fabs(yawcontrol) > 0.5:
            yawcontrol = 0.5 * np.sign(yawcontrol)
        '''

        #if math.fabs(yawcontrol - self.tYaw) > 0.05 :
        #    yawcontrol = 


        if math.fabs(yawcontrol) > 0.3:
            yawcontrol = 0.3 * np.sign(yawcontrol)


        print (xVel, zVel, yawcontrol)
        print ('"""""""')

        yVel = np.sign(yawcontrol) * 0.03


        self.interface.sendCMDVel(xVel, yVel, zVel*1.2, yawcontrol)

        self.tYaw = yawcontrol

        '''
        if math.fabs(ux) > 0.3 :
            ux = 0.3 * np.sign(ux)
        if math.fabs(uy) > 0.3 :
            uy = 0.3 * np.sign(uy)
        if math.fabs(uz) > 0.3 :
            uy = 0.3 * np.sign(uy)
        '''
        ###1pt
        #self.interface.sendCMDVel(ux, uy, uz, 0)
        #print (ux, uy, uz)
        

        #Final position prediction
        #self.tpose.x = L * math.cos(yawcontrol) + pose3d.x
        #self.tpose.y = L * math.sin(yawcontrol) + pose3d.y
        #self.tpose.z = zVel*0.08 + pose3d.z

    def YawTemporalFilter(self):
        #Pesos: 1.2, 0.6, 0.3, 0.2, 0.1
        #SumPesos: 2.3
        yaw = self.yawFilterArray[0] * 1.0
        yaw += self.yawFilterArray[1] * 0.6
        yaw += self.yawFilterArray[2] * 0.4
        yaw += self.yawFilterArray[3] * 0.2
        yaw += self.yawFilterArray[4] * 0.1
        yaw /= 2.3
        return yaw

    def setVel(self, v, w):
        self.Vel = v
        self.AngVel = w

    def setAngVel(self, w):
        self.AngVel = w

    def setLinVel(self, v):
        self.Vel = v

    def qtoyaw(self, q0,q1,q2,q3):
        #Transforms quaternions to (yaw,pitch,roll)
        yaw = math.atan2(2.0*(q0*q3 + q1*2), 1 - 2*(q2**2 + q3**2));
        return yaw  #[-pi,pi]

    def distance(self, pose3d1, pose3d2):
        #Distance between drone position and next point
        d = math.sqrt((pose3d1.x - pose3d2.x)**2 + (pose3d1.y - pose3d2.y)**2 + (pose3d1.z - pose3d2.z)**2)
        return d


    def module(self,x,y,z):
        return math.sqrt((x**2)+(y**2)+(z**2))


    '''
    def errormatrix(self, pose3d, yaw):
        p = self.path[self.step]
        A = [[math.cos(p.q0), math.sin(p.q0), 0],
            [-math.sin(p.q0), math.cos(p.q0), 0]
            [0, 0, 1]]
        B = [[p.x - pose3d.x], [p.y - pose3d.y], [p.q0 - yaw]]
        return np.dot(A,B)
    '''










