import sys, traceback, Ice
import jderobot
import numpy as np
import threading
import cv2

class Control():

    def __init__(self):
        self.lock = threading.Lock()
        self.effectON = 'False'

        try:
            ic = Ice.initialize(sys.argv)
            properties = ic.getProperties()
            camera = ic.propertyToProxy("Camarareal.Camera.Proxy")
            self.cameraProxy = jderobot.CameraPrx.checkedCast(camera)
            if self.cameraProxy:
                self.image = self.cameraProxy.getImageData("RGB8")
                self.height= self.image.description.height
                self.width = self.image.description.width
            else:
                print 'Interface camera not connected'

        except:
            traceback.print_exc()
	    exit()
            status = 1

    def update(self):
        if self.cameraProxy:
            self.lock.acquire()
            print 'updtcontrol'
            self.image = self.cameraProxy.getImageData("RGB8")
            self.height= self.image.description.height
            self.width = self.image.description.width
            self.lock.release()

    def getImage(self):
        if self.cameraProxy:
            self.lock.acquire()
            print 'getimage'
            image = np.zeros((self.height, self.width, 3), np.uint8)
            image = np.frombuffer(self.image.pixelData, dtype=np.uint8)
            image.shape = self.height, self.width, 3
            self.lock.release()
            if self.effectON:
                return self.opencvtest(image)
            else:
                return image;

    def effect(self):
        self.effectON = not self.effectON

    def opencvtest(self, img):
        image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        return image
