# started experiments with f360 driver-script


# There is a lot of code copied from stackoverflow, autodesk forums, etc.
# windows only yet


import adsk.fusion, adsk.core, traceback
import math

from .lib import joystickapi
from .lib.conversions import *
from .lib import fusion360utils as futil
import msvcrt
import time
import inspect, os, sys


# todo move to config

# ranges, centers and deadzones of axes

zoomRange = [-32767,32767]
yawRange = [-32767,32767]
trxRange = [-32767,32767]
tryRange = [-32767,32767]

zoomCenter = 0
yawCenter = 0
trxCenter = 0
tryCenter = 0

zoomDZ = [-2048,2048]
yawDZ = [-2048,2048]
trxDZ = [-2048,2048]
tryDZ = [-2048,2048]




class Joystick:
    """This is wrapper class for joystick

    Attributes
    ----------
    supportedOS : list
        list with supported os


    Constructor
    -----------
    requires only id of joystick in system 
    todo: maybe in other systems name or uuid required

    Methods
    -------
    getAxis(str: axis)->int
        returns integer value of axis
    """
    osn=None
    supportedOS=['nt']
    

    axIndex=["X","Y","Z","R","U","V"]

    def __init__(self,id=0):
        """
        initializing joystick. Throws "Unsopported os" if os not supported
        """
        self.osn=os.name

        if self.osn not in self.supportedOS:
            raise Exception("Unsupported os")

        self.id=id
        ret, caps=joystickapi.joyGetDevCaps(id)
        
        self.ManufacturerId = caps.wMid
        self.ProductId = caps.wPid
        self.ProductName = caps.szPname
        self.NumButtons = caps.wNumButtons
        self.PeriodMin = caps.wPeriodMin
        self.PeriodMax = caps.wPeriodMax
        self.Caps = caps.wCaps
        self.MaxAxes = caps.wMaxAxes
        self.NumAxes = caps.wNumAxes
        self.MaxButtons = caps.wMaxButtons
     
        self.rangeX=[caps.wXmin,caps.wXmax]
        self.rangeY=[caps.wYmin,caps.wYmax]
        self.rangeZ=[caps.wZmin,caps.wZmax]

        self.rangeR=[caps.wRmin,caps.wRmax]
        self.rangeU=[caps.wUmin,caps.wUmax]
        self.rangeV=[caps.wVmin,caps.wVmax]

        self.ranges=[ self.rangeX, self.rangeY, self.rangeZ, self.rangeR, self.rangeU, self.rangeV]
        


    def getAxesRaw(self) -> list:
        out=[]
        ret, io = joystickapi.joyGetPosEx(self.id)
        if ret:        
            # X Y Z R U V POV
            axes = [
                io.dwXpos,
                io.dwYpos,
                io.dwZpos,
                io.dwRpos,
                io.dwUpos,
                io.dwVpos,
                io.dwPOV
            ]

            return axes
        #else:
        #    raise Exception("Joystick read error")
        



        

    def getAxisRaw(self,axis: str) -> int:
        """Returns value of defined axis

        axes:

        dwXpos
        Current X-coordinate.
        
        dwYpos
        Current Y-coordinate.
        
        dwZpos
        Current Z-coordinate.
        
        dwRpos
        Current position of the rudder or fourth joystick axis.
        
        dwUpos
        Current fifth axis position.
        
        dwVpos
        Current sixth axis position.

        dwPOV
        Current position of the point-of-view control. Values for this member are in the range 0 through 35,900. These values represent the angle, in degrees, of each view multiplied by 100.

        source: https://docs.microsoft.com/en-us/previous-versions/dd757112(v=vs.85)
        """
        out=0
        availableAxes = ["dwXpos","dwYpos","dwZpos","dwRpos","dwUpos","dwVpos","dwPOV"]
        if axis in availableAxes or axis=="list":
            axes = self.getAxesRaw()
            return axes[availableAxes.index(axis)]
        else:
            raise Exception("Axis doesnt exists")

        

    def getAxes(self) -> list:
        axesRaw = self.getAxesRaw()
        out=[]      
        

        for i in range(0,len(axesRaw)):            
            out.append(int(correctAxis(axesRaw[i-1],self.ranges[i-1],0.05)))

        return out
        






joy = Joystick()

def run(context):
# This section executes once on script start 
    ui = None
    app = adsk.core.Application.get()
    ui = app.userInterface
    futil.log(str("Joystick driver v"+"/version/"+" started"))
    futil.log("START")


    # this found there https://github.com/Rabbid76/python_windows_joystickapi

    numOfJoysticks = joystickapi.joyGetNumDevs()
    ret, caps, startinfo = False, None, None
    for id in range(numOfJoysticks):
        ret, caps = joystickapi.joyGetDevCaps(id)
        if ret:
            ui.messageBox(str("Using gamepad: " + caps.szPname))
            ret, startinfo = joystickapi.joyGetPosEx(id)
            break
    else:
        ui.messageBox(str("no gamepad detected"))

        
# This section executes once on script start 


# Loop starts

    while True:      
        


        futil.log(str(joy.getAxes()))

        deg = 0 #joy.getAxes()["V"]/52428 


        app: adsk.core.Application = adsk.core.Application.get()
        ui = app.userInterface
        # viewport
        vp: adsk.core.Viewport = app.activeViewport
        cam: adsk.core.Camera = vp.camera
        vecUp: adsk.core.Vector3D = adsk.core.Vector3D.create(0,0,10000000)


        target: adsk.core.Point3D = cam.target
        # matrix3d
        mat: adsk.core.Matrix3D = adsk.core.Matrix3D.create()

        mat.setToRotation(math.radians(deg), vecUp, target)
        # update camera
        cam.isSmoothTransition = False
        
        eye: adsk.core.Point3D = vp.camera.eye
        eye.transformBy(mat)
        cam.eye = eye

        # zoom = cam.viewExtents

        # if axisXYZRUV[0]>1024 or axisXYZRUV[0]<-1024:
        #     zoom = zoom - (axisXYZRUV[0]/10000)*(zoom/100)

        # if zoom<0:
        #     zoom=0.001



        #futil.log(str(axisXYZRUV[0])+"|||||"+str(cam.viewExtents))
        # cam.viewExtents = zoom
        vp.camera = cam
        vp.refresh()
        
        adsk.doEvents()
