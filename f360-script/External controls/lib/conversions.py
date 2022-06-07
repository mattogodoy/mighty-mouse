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