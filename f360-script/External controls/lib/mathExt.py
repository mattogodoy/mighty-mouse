import math
from msilib.schema import RadioButton


def scale(val,minIn,maxIn,minOut,maxOut):
    """same as map() in c++
    """
    return (val - minIn) * (maxOut - minOut) / (maxIn - minIn) + minOut



def correctAxis(value: int,rang: list,deadzone: float,)-> int:
    """Corrects axis value (its hard to explain what it does) returns 20bit int (-2^19 ; 2^19)
    Parameters
    ----------
    value: int 
        value to correct
    
    range: list
        range of axis ( [from,to] )
    
    deadzone: float
        zone (from center) where value will be always zero 
    

    """
    out=0
    


    out=scale(value,rang[0],rang[1],-524287,524287)
    if out<-524287*deadzone or out>+524287*deadzone:
        out=out
    else:
        out=0

    return out

def precissionEqual(val1,val2,epsilon):
    vmin=vmax=val1-epsilon,val1+epsilon
    if val2>=vmin and val2<=vmax:
        return True
    else:
        return False

def getVectorAngles(x,y,z):
    """returns angles in radians
    """
    try:
        angleX = math.atan(z/y)
    except ZeroDivisionError:
        angleX=0
    try:
        angleY = math.atan(z/x)
    except ZeroDivisionError:
        angleY=0
    try:
        angleZ = math.atan(y/x)
    except ZeroDivisionError:
        angleZ=0
    return angleX,angleY,angleZ

def getPerpendicularVector(x,y,z):
    length=(x*x+y*y+z*z)**0.5
    oAngleX,oAngleY,oAngleZ = getVectorAngles(x,y,z)
    angleX, angleY, angleZ = math.pi/2-oAngleX, math.pi/2-oAngleY, math.pi/2-oAngleZ
    dotX,dotY,dotZ = math.cos(angleX)*length,math.cos(angleY)*length,math.cos(angleZ)*length

    return dotX,dotY,dotZ
