import numpy as np
from feather.algebra import translate, rotate, scale
from feather.vector3 import Vec3

class Transform():
    def __init__(self):
        self.position = Vec3(0.0, 0.0, 0.0)
        self.scaling = Vec3(1.0, 1.0, 1.0)
        self.rotation = Vec3(0.0, 0.0, 0.0)

    def setPosition(self, x, y, z):
        """Sets the object's position and returns the object"""
        self.position.x = x
        self.position.y = y
        self.position.z = z
        return self

    def getPosition(self):
        return self.position

    def translate(self, x, y, z):
        """Translates the object by the given amount and returns the object"""
        self.position.x += x
        self.position.y += y
        self.position.z += z
        return self

    def getPositionMatrix(self):
        return translate(self.position.x, self.position.y, self.position.z)

    def setScaling(self, x, y, z):
        """Sets the object's scaling and returns the object"""
        self.scaling.x = x
        self.scaling.y = y
        self.scaling.z = z
        return self

    def getScaling(self):
        return self.scaling

    def getScalingMatrix(self):
        return scale(self.scaling.x, self.scaling.y, self.scaling.z)

    def setRotationAxisAround(self, angle, axisX, axisY, axisZ, x, y, z):
        position4 = np.array([self.position.x, self.position.y, self.position.z, 1.0])
        rotatedPosition4 = rotate(angle, axisX, axisY, axisZ).dot(position4)
        self.position = np.array([rotatedPosition4[0], rotatedPosition4[1], rotatedPosition4[2]])
        self.translate(x, y, z)

    def setRotationXAround(self, angle, x, y, z):
        self.setRotationAxisAround(angle, 1.0, 0.0, 0.0, x, y, z)

    def setRotationYAround(self, angle, x, y, z):
        self.setRotationAxisAround(angle, 0.0, 1.0, 0.0, x, y, z)

    def setRotationZAround(self, angle, x, y, z):
        self.setRotationAxisAround(angle, 0.0, 0.0, 1.0, x, y, z)

    def setRotation(self, xAngle, yAngle, zAngle):
        """Sets the rotation of the object along each world axis"""
        self.rotation.x = xAngle
        self.rotation.y = yAngle
        self.rotation.z = zAngle
        return self
    
    def setRotationX(self, angle):
        """Sets the object's rotation around the world X axis and returns the object"""
        self.rotation.x = angle
        return self
    
    def setRotationY(self, angle):
        """Sets the object's rotation around the world Y axis and returns the object"""
        self.rotation.y = angle
        return self

    def setRotationZ(self, angle):
        """Sets the object's rotation around the world Z axis and returns the object"""
        self.rotation.z = angle
        return self

    def addRotation(self, xAngle, yAngle, zAngle):
        """Adds to the object's rotation around each world axis and returns the object"""
        self.rotation.x += xAngle
        self.rotation.y += yAngle
        self.rotation.z += zAngle
        return self

    def addRotationX(self, angle):
        """Adds to the object's rotation around the world X axis and returns the object"""
        self.rotation.x += angle
        return self

    def addRotationY(self, angle):
        """Adds to the object's rotation around the world Y axis and returns the object"""
        self.rotation.y += angle
        return self

    """Adds to the object's rotation around the world Z axis and returns the object"""
    def addRotationZ(self, angle):
        self.rotation.z += angle
        return self

    def getRotationMatrix(self):
        #TODO: use a cache system to reduce computations
        return rotate(self.rotation.x, 1.0, 0.0, 0.0).dot(
                rotate(self.rotation.y, 0.0, 1.0, 0.0)).dot(
                rotate(self.rotation.z, 0.0, 0.0, 1.0))

    def getMatrix(self):
        ### FIXME: le scaling doit être fait avant le positionnement
        return self.getRotationMatrix().dot(self.getPositionMatrix()).dot(self.getScalingMatrix())
