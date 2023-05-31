import os
from utils import *

class sound:
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.happy = None
        self.silly = None
        self.curious = None
        self.smile = None
        self.storeSound()
    
    def storeSound(self):
        dir = os.getcwd() + self.dir_path 
        for Sound_path in os.listdir(dir):
            Sound = os.path.join(dir,Sound_path)
            if os.path.isfile(Sound):
                if 'happy' in Sound:
                    self.happy = Sound
                elif 'silly' in Sound:
                    self.silly = Sound
                elif 'curious' in Sound:
                    self.curious = Sound
                else:
                    self.smile = Sound
            
    def getHappySound(self):
        return self.happy
    def getSillySound(self):
        return self.silly
    def getCuriousSound(self):
        return self.curious
    def getSmileSound(self):
        return self.smile
        