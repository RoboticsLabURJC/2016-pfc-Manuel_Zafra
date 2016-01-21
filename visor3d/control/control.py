import sys, traceback, Ice
import jderobot
import numpy as np
import threading
import cv2
import pickle
from matplotlib import pyplot as plt

class Control():

    def __init__(self):
        self.lock = threading.Lock()
        try:
            ic = Ice.initialize(sys.argv)
            properties = ic.getProperties()

            #Connection to ICE interfaces
            basepose3D = ic.propertyToProxy("Visor3D.Pose3D.Proxy")
            self.pose3DProxy=jderobot.Pose3DPrx.checkedCast(basepose3D)
            if self.pose3DProxy:
                self.pose=jderobot.Pose3DData()
            else:
                print 'Interface pose3D not connected'

            baseroute = ic.propertyToProxy("Visor3D.Route.Proxy")
            self.routeProxy=jderobot.Pose3DPrx.checkedCast(baseroute)
            if self.routeProxy:
                self.route=jderobot.Pose3DData()
            else:
                print 'Interface RoutePose3D not connected'

        except:
            traceback.print_exc()
	    exit()
            status = 1

    def update(self):
        if self.pose3DProxy:
            self.lock.acquire()
            self.pose=self.pose3DProxy.getPose3DData()
            self.route=self.routeProxy.getPose3DData()
            self.lock.release()

    def getPose3D(self):
        if self.pose3DProxy:
            self.lock.acquire()
            tmp=self.pose
            self.lock.release()
            return tmp

    def getRoute(self):
        if self.routeProxy:
            self.lock.acquire()
            tmp=self.route
            self.lock.release()
            return tmp

