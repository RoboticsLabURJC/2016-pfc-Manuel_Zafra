import sys
import jderobot
import threading
import Ice

class Control():

    def __init__(self):

        self.lock = threading.Lock()

        try:
            ic = Ice.initialize(sys.argv)
            properties = ic.getProperties()
            basecamera = ic.propertyToProxy("Camarareal.Camera.Proxy")
            self.cameraProxy = jderobot.CameraPrx.checkedCast(basecamera)

            if self.cameraProxy:
                self.image = self.cameraProxy.getImageData("RGB8")
                self.height= self.image.description.height
                self.width = self.image.description.width

                self.trackImage = np.zeros((self.height, self.width,3), np.uint8)
                self.trackImage.shape = self.height, self.width, 3

                self.thresoldImage = np.zeros((self.height, self.width,1), np.uint8)
                self.thresoldImage.shape = self.height, self.width, 1

                self.filterValues = ColorFilterValues()

            else:
                print 'Interface camera not connected'

        except:
            traceback.print_exc()
	    exit()
            status = 1

    def update(self):
        self.lock.acquire()
        if self.cameraProxy:
            self.image = self.cameraProxy.getImageData("RGB8")
            self.height= self.image.description.height
            self.width = self.image.description.width
        self.lock.release()

    def getImage(self):
        if self.cameraProxy:
            self.lock.acquire()
            img = np.zeros((self.height, self.width, 3), np.uint8)
            img = np.frombuffer(self.image.pixelData, dtype=np.uint8)
            img.shape = self.height, self.width, 3
            self.lock.release()
            return img;


