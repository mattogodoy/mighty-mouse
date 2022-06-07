# started experiments with f360 driver-script


# There is a lot of code copied from stackoverflow, autodesk forums, etc.
# windows only yet


import adsk.fusion, adsk.core, traceback
import math

from .lib import joystickapi
from .lib import fusion360utils as futil
import msvcrt
import time
import inspect, os, sys




def run(context):
# This section executes once on script start 
    ui = None
    app = adsk.core.Application.get()
    ui = app.userInterface
    ui.messageBox('bruh it started')


    num = joystickapi.joyGetNumDevs()
    ret, caps, startinfo = False, None, None
    for id in range(num):
        ret, caps = joystickapi.joyGetDevCaps(id)
        if ret:
            ui.messageBox(str("gamepad detected: " + caps.szPname))
            ret, startinfo = joystickapi.joyGetPosEx(id)
            break
    else:
        ui.messageBox(str("no gamepad detected"))
# This section executes once on script start 


# Loop starts

    while True:      
        run = ret
        ret, info = joystickapi.joyGetPosEx(id)
        if ret:        
            axisXYZRUV = [info.dwXpos-startinfo.dwXpos, info.dwYpos-startinfo.dwYpos, info.dwZpos-startinfo.dwZpos,
            info.dwRpos-startinfo.dwRpos, info.dwUpos-startinfo.dwUpos, info.dwVpos-startinfo.dwVpos]

        futil.log(str(axisXYZRUV))


        deg = axisXYZRUV[5]/2000 #Angle of one step - degree




        app: adsk.core.Application = adsk.core.Application.get()
        ui = app.userInterface
        # viewport
        vp: adsk.core.Viewport = app.activeViewport
        cam: adsk.core.Camera = vp.camera
        vecUp: adsk.core.Vector3D = cam.upVector
        target: adsk.core.Point3D = cam.target
        # matrix3d
        mat: adsk.core.Matrix3D = adsk.core.Matrix3D.create()
        rad = math.radians(deg)
        mat.setToRotation(rad, vecUp, target)
        # update camera
        cam.isSmoothTransition = False
        eye: adsk.core.Point3D = vp.camera.eye
        eye.transformBy(mat)
        cam.eye = eye
        vp.camera = cam
        vp.refresh()
        adsk.doEvents()
