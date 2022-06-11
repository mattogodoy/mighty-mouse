
from . import fusion360utils as futil



class Logger:
    def __init__(self,mode:str="f360cmd"):
        self.mode="f360cmd"

    def print(self,message:any=""):
        message=str(message)
        futil.log(message)