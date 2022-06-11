from . import joystickapi
import os
from .mathExt import *

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
        
        if str(type(axesRaw))=="<class 'NoneType'>":
            return [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        for i in range(0,len(axesRaw)):            
            out.append(int(correctAxis(axesRaw[i-1],self.ranges[i-1],0.05)))

        return out