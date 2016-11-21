#!/usr/bin/python

import threading
import time
from datetime import datetime
import sys, traceback
import Ice
import jderobot
import numpy as np

t_cycle = 800 # ms

#Este programa recoge los datos servidos por replayer2 y los guarda en un fichero de texto

try:
    ic = Ice.initialize(sys.argv)
    properties = ic.getProperties()

    #------- POSE3D ---------
    basepose3D = ic.propertyToProxy("Path.Pose3D.Proxy")
    pose3DProxy=jderobot.Pose3DPrx.checkedCast(basepose3D)
    if pose3DProxy:
        realpose=jderobot.Pose3DData()
    else:
        print 'Interface pose3D not connected'

except:
    traceback.print_exc()
    exit()
    status = 1
print 'holi'
while(pose3DProxy):

    start_time = datetime.now()
    print 'holi2'
    if pose3DProxy:
        pose=pose3DProxy.getPose3DData()
        pathfile = open('path.txt', 'a')
        pathfile.write('%f %f %f\n' %(pose.x, pose.y, pose.z))
        pathfile.close()
    end_time = datetime.now()

    dt = end_time - start_time
    dtms = ((dt.days * 24 * 60 * 60 + dt.seconds) * 1000 
        + dt.microseconds / 1000.0)
        
    if(dtms < t_cycle):
        time.sleep((t_cycle - dtms) / 1000.0);



