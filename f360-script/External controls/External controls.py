# started experiments with f360 driver-script


# There is a lot of code copied from stackoverflow, autodesk forums, etc.
# windows only yet

import adsk.fusion, adsk.core, traceback
import math

from .lib import joystickapi
from .lib.mathExt import *
from .lib.Joystick import *
from .lib.logger import *

from .lib import fusion360utils as futil
from .config import *
from . import commands


import msvcrt
import time
import inspect, os, sys

logger=Logger()


def greeting():
    logger.print("------Starting------")
    logger.print("f360 joystick driver")
    logger.print(f"version, {VERSION}. By {AUTHOR}.")
        


def transformCameraByMatrix(camera: adsk.core.Camera, matrix: adsk.core.Matrix3D):
        eye: adsk.core.Point3D = camera.eye
        eye.transformBy(matrix)
        camera.eye = eye

def transformCameraByVector(camera: adsk.core.Camera, vector: adsk.core.Vector3D):
        eye: adsk.core.Point3D = camera.eye
        eye.translateBy(vector)
        camera.eye = eye


    
def changeCameraZoom(camera: adsk.core.Camera,zoom):
    zoomOld = camera.viewExtents
    if zoom<0:
        zoom=0.001
    camera.viewExtents = zoom

numOfJoysticks = joystickapi.joyGetNumDevs()


joy = None

def run(context):

    try:
        # This will run the start function in each of your commands as defined in commands/__init__.py
        commands.start()

    except:
        futil.handle_error('run')

# This section executes once on script start 
    ui = None
    app: adsk.core.Application = adsk.core.Application.get()
    ui = app.userInterface
    greeting()

    if numOfJoysticks==0:
        raise Exception("No joystick")
    else:
        joy = Joystick()

    # this found there https://github.com/Rabbid76/python_windows_joystickapi


    ret, caps, startinfo = False, None, None
    for id in range(numOfJoysticks):
        ret, caps = joystickapi.joyGetDevCaps(id)
        if ret:
            ui.messageBox(str("Using gamepad: " + caps.szPname))
            ret, startinfo = joystickapi.joyGetPosEx(id)
            break
        else:
           ui.messageBox(str("no gamepad detected"))

    first=True
# This section executes once on script start 


# Loop starts

    while True:      
        # viewport
        vp: adsk.core.Viewport = app.activeViewport
        cam: adsk.core.Camera = vp.camera
        vecUp: adsk.core.Vector3D = cam.upVector
        target: adsk.core.Point3D = cam.target
        eye: adsk.core.Point3D = cam.eye



        eTvector=eye.vectorTo(target)
        angle1 = eTvector.angleTo(vecUp)
        dx,dy,dz = getPerpendicularVector(vecUp.x, vecUp.y, vecUp.z)
        perpendicular = adsk.core.Point3D.create(dx,dy,dz)
        perpendicular=perpendicular.asVector()

        angle2=vecUp.angleTo(perpendicular)


        if numOfJoysticks==0:
            raise Exception("No joystick")
        

        deg = (joy.getAxes()[6]/262144)
        deg=deg*deg*deg

        zoom = cam.viewExtents
        if cam.cameraType==0:
            zoom = zoom-joy.getAxes()[1]/2621*zoom/5000
        else:
            zoom = zoom-joy.getAxes()[1]/26214400
        

        changeCameraZoom(cam,zoom)

        # futil.log( str(str(joy.getAxes()) +"|"+ str(cam.viewExtents))) # all axes output
        logger.print(
            "vecUp - target angle: "+str(math.degrees(angle1))+ "\n"+
            "vecUp - calcul angle: "+str(math.degrees(angle2))+ "\n"+
            str(perpendicular.x)+"|"+str(perpendicular.y)+"|"+str(perpendicular.z)
            )
        

        # matrix3d
        mat: adsk.core.Matrix3D = adsk.core.Matrix3D.create()

        mat.setToRotation(math.radians(deg), vecUp, target)
        # update camera
        cam.isSmoothTransition = False
        
        transformCameraByMatrix(cam,mat)

        transformCameraByVector(cam,perpendicular)







        #futil.log(str(axisXYZRUV[0])+"|||||"+str(cam.viewExtents))
        # cam.viewExtents = zoom
        vp.camera = cam
        vp.refresh()
        
        adsk.doEvents()
