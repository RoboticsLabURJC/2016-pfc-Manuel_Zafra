import sys, traceback, Ice
import jderobot
import numpy as np
import threading
import cv2
from matplotlib import pyplot as plt

class Control():

    def __init__(self):
        self.lock = threading.Lock()
        self.img = np.zeros((350,350,3), np.uint8)
        cv2.line(self.img,(0,0),(200,200),(255,0,0),1)
        #self.drawAxis()

    def 3dto2d(self, x, y ,z):
        point =
        return point

    def update(self):
        self.lock.acquire()
        print 'updtcontrol'
        self.lock.release()

    def getImage(self):
        self.lock.acquire()
        print 'getimg'
        self.lock.release()
        return self.img

    def drawAxis(self):
        cv2.line(self.img,(0,0),(0,0),(255,0,0),5)
        cv2.line(self.img,(0,0),(70,0),(0,255,0),5)
        cv2.line(self.img,(0,0),(0,70),(0,0,255),5)
