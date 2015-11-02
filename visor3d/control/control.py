import sys, traceback, Ice
import jderobot
import numpy as np
import threading
import cv2
from matplotlib import pyplot as plt

class Control():

    def __init__(self):
        self.lock = threading.Lock()
        try:
            ic = Ice.initialize(sys.argv)
            properties = ic.getProperties()
            basepose3D = ic.propertyToProxy("Visor3D.Pose3D.Proxy")
            self.pose3DProxy=jderobot.Pose3DPrx.checkedCast(basepose3D)
            if self.pose3DProxy:
                self.pose=jderobot.Pose3DData()
            else:
                print 'Interface pose3D not connected'

        except:
            traceback.print_exc()
	    exit()
            status = 1

    def update(self):
        print 'updcontrol'
        if self.pose3DProxy:
            print 'updlockon'
            self.lock.acquire()
            self.pose=self.pose3DProxy.getPose3DData()
            self.lock.release()
            print 'updlockoff'
    def getPose3D(self):
        if self.pose3DProxy:
            print 'getlockon'
            self.lock.acquire()
            tmp=self.pose
            self.lock.release()
            print 'getlockoff'
            return tmp

    def getRoute(self):
        #self.lock.acquire()
        print 'getroute'
        #self.lock.release()
