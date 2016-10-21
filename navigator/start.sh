#!/bin/bash 

gzserver ../gazebo/AprilTagsFlat.world &
./cam_autoloc --Ice.Config=cam_autoloc.cfg &
./navigator.py --Ice.Config=nav.cfg

