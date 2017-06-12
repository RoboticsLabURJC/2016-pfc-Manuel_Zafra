#!/usr/bin/env python3
import sys, traceback, Ice
import easyiceconfig as EasyIce
import jderobot
import numpy as np
import threading

class Interfaces():

    ARDRONE1=0
    ARDRONE2=1
    ARDRONE_SIMULATED=10
    #flat
    path = np.array([(-5.16,-1.92,1.38),(-4.28,-0.61,1.38),(-3.3,-0.61,1.38),
            (-2.72,-2.72,1.38),(-2.52,-3.74,1.58),(-2.52,-5.44,1.58),
            (-1.59,-6.87,1.22),(-1.14,-5.9,1.45),(-2.52,-5.04,1.52)])
            #(-2.52,-2.34,1.51),(-0.75,-2.34,1.51)]

    def __init__(self):
        self.lock = threading.Lock()
        try:
            ic = EasyIce.initialize(sys.argv)
            properties = ic.getProperties()

            #Connection to ICE interfaces

            #------- POSE3D ---------
            basepose3D = ic.propertyToProxy("Navigator.Pose3D.Proxy")
            self.pose3DProxy=jderobot.Pose3DPrx.checkedCast(basepose3D)
            if self.pose3DProxy:
                self.pose=jderobot.Pose3DData()
            else:
                print ('Interface pose3D not connected')

            #-------- CMDVEL ----------
            basecmdVel = ic.propertyToProxy("Navigator.CMDVel.Proxy")
            self.cmdVelProxy=jderobot.CMDVelPrx.checkedCast(basecmdVel)
            if not self.cmdVelProxy:
                print ('Interface cmdVel not connected')

            #------- NAVDATA ----------
            basenavdata = ic.propertyToProxy("Navigator.Navdata.Proxy")
            self.navdataProxy = jderobot.NavdataPrx.checkedCast(basenavdata)
            if self.navdataProxy:
                self.navdata=self.navdataProxy.getNavdata()
                if self.navdata.vehicle == self.ARDRONE_SIMULATED :
                    self.virtualDrone = True
                else:
                    self.virtualDrone = False
            else:
                print ('Interface navdata not connected')
                self.virtualDrone = True

            #--------- EXTRA ----------
            baseextra = ic.propertyToProxy("Navigator.Extra.Proxy")
            self.extraProxy=jderobot.ArDroneExtraPrx.checkedCast(baseextra)
            if not self.extraProxy:
                print ('Interface ardroneExtra not connected')


            #-------- CAMERA ----------
            basecamera = ic.propertyToProxy("Navigator.Camera.Proxy")
            self.cameraProxy = jderobot.CameraPrx.checkedCast(basecamera)

            if self.cameraProxy:
                self.image = self.cameraProxy.getImageData("RGB8")
                self.height= self.image.description.height
                self.width = self.image.description.width

        except:
            traceback.print_exc()
            exit()
            status = 1

        self.pause = True
        #self.takeoff()

    def update(self):
        self.lock.acquire()
        self.updateCamera()
        self.updateNavdata()
        self.updatePose()
        self.lock.release()

    def updateCamera(self):
        if self.cameraProxy:
            self.image = self.cameraProxy.getImageData("RGB8")
            self.height= self.image.description.height
            self.width = self.image.description.width

    def updateNavdata(self):
        if self.navdataProxy:
            self.navdata=self.navdataProxy.getNavdata()

    def updatePose(self):
        if self.pose3DProxy:
            self.pose=self.pose3DProxy.getPose3DData()

    def getNavdata(self):
        if self.navdataProxy:
            self.lock.acquire()
            tmp=self.navdata
            self.lock.release()
            return tmp
        else:
            return None

    def getPose3D(self):
        if self.pose3DProxy:
            self.lock.acquire()
            tmp=self.pose
            self.lock.release()
            return tmp
        else:
            return None

    def getImage(self):
        if self.cameraProxy:
            self.lock.acquire()
            img = np.zeros((self.height, self.width, 3), np.uint8)
            img = np.frombuffer(self.image.pixelData, dtype=np.uint8)
            img.shape = self.height, self.width, 3
            self.lock.release()
            return img;
        else:
            return None

    '''
    def takeoff(self):
        if self.extraProxy:
            self.lock.acquire()
            self.extraProxy.takeoff()
            self.lock.release()
    '''

    def sendCMDVel(self,vx,vy,vz,yaw):
        if not self.pause:
            cmd=jderobot.CMDVelData()
            cmd.linearX=vx
            cmd.linearY=vy
            cmd.linearZ=vz
            cmd.angularZ=yaw
            cmd.angularX=cmd.angularY=0.0
        else:
            cmd=jderobot.CMDVelData()
            cmd.linearX=0
            cmd.linearY=0
            cmd.linearZ=0
            cmd.angularZ=0
            cmd.angularX=cmd.angularY=0

        if self.cmdVelProxy:
            self.lock.acquire();
            self.cmdVelProxy.setCMDVelData(cmd)
            self.lock.release();

    def startdrone(self):
        self.pause = False

    def pausedrone(self):
        self.pause = True

    def landdrone(self):
        self.pause = True
        if self.extraProxy:
            self.lock.acquire()
            self.extraProxy.land()
            self.lock.release()

    def togglecam(self):
        if self.extraProxy:
            self.lock.acquire()
            self.extraProxy.toggleCam()
            self.lock.release()

    def takeoffdrone(self):
        self.pause = True
        if self.extraProxy:
            self.lock.acquire()
            self.extraProxy.takeoff()
            self.lock.release()


