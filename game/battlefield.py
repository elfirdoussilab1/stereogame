from feather.shapes.land import Land
from feather.vector3 import Vec3
import numpy as np


class Battlefield(Land):
    
    def __init__(self, name, size_x, size_y, size_z, player1, player2, scene = None):
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        self.player1 = player1
        self.player2 = player2
        Land.__init__(self, name, False, True, True, True, scene)
        self.setScaling(size_x, size_y, size_z)
        self.areViewsSwitched = False


    def getSizex(self):
        return self.size_x

    def getSizey(self):
        return self.size_y

    def getSizez(self):
        return self.size_z
    
    

    def isCollision(self, r, center): # cette fonction prend en paramètres un poins dans l'espace
                            # et renvoie True s'il y a collision entre ce point et la
                            #  battlefield
        x,y,z = center.x, center.y, center.z

        if x+r >= self.size_x or x-r <= -self.size_x:
            return True
        if y+r >= self.size_y or y-r <= -self.size_y:
            return True
        if z+r >= self.size_z or z-r <= -self.size_z:
            return True

        return False

    def whereCollision(self, r, center):
        x,y,z = center.x, center.y, center.z
        if x+r >= self.size_x:
            return "right"
        elif x-r <= -self.size_x:
            return "left"
        elif y+r >= self.size_y:
            return "top"
        elif y-r <= -self.size_y:
            return "bottom"
        elif z+r >= self.size_z:
            return "front"
        elif z-r <= -self.size_z:
            return "back"
        else:
            return "No Collision"

    def normalVector(self, face):
        if face == "right":
            return Vec3(-1,0,0)
        elif face == "left":
            return Vec3(1,0,0)
        elif face == "top":
            return Vec3(0,-1,0)
        elif face == "bottom":
            return Vec3(0,1,0)
        elif face == "front":
            return Vec3(0,0,-1)
        elif face == "back":
            return Vec3(0,0,1)
        else:
            return Vec3(0,0,0)
        
    
    
    



