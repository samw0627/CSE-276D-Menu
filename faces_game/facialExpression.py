import os
from utils import * 

class facialExpression:
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.happy = {}
        self.silly = {}
        self.curious = {}
        self.smile = {}
        self.storeFaces()
        
    def storeFaces(self):
        dir = os.getcwd()+self.dir_path
        for img_path in os.listdir(dir):
            img = os.path.join(dir, img_path)
            if os.path.isfile(img):
                # file_name, _ = os.path.splitext(img)
                if 'happy' in img:
                    if '1' in img:
                        self.happy[OPEN] = img
                    else:
                        self.happy[BLINK]= img
                    
                elif 'silly' in img:
                    if '1' in img:
                        self.silly[OPEN] = img
                    else:
                        self.silly[BLINK]= img
                elif 'curious' in img:
                    if '1' in img:
                        self.curious[OPEN] = img
                    else:
                        self.curious[BLINK]= img
                else:
                    if '1' in img:
                        self.smile[OPEN] = img
                    else:
                        self.smile[BLINK]= img
    
    def getHappyFace(self):
        return self.happy
    def getSillyFace(self):
        return self.silly
    def getCuriousFace(self):
        return self.curious
    def getSmileFace(self):
        return self.smile
    
# if __name__ == "__main__":
#     faces = facialExpression("/face_img/png")
#     cv2.imshow('png',faces.smileFace())
#     cv2.waitKey(0) 
#     cv2.destroyAllWindows()