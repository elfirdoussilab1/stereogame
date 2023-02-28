import numpy as np
from pygame.math import Vector3
from feather.transform import Transform
from feather.algebra import rotate, lookat
from feather.projections import perspective
from feather.vector3 import Vec3

class Camera(Transform):
    def __init__(self, fov, aspectRatio):
        Transform.__init__(self)
        self.projection = perspective(fov, aspectRatio, 0.1, 100)
        self.target = Vector3(0, 0, 0)
        self.position = Vec3(0.0, 0.0, -1.0)
        self.view_matrix = self.computeViewMatrix()

    def computeViewMatrix(self):
        self.view_matrix = lookat(self.position, self.target)
        return self.view_matrix

    def setPosition(self, x, y, z):
        self.computeViewMatrix()
        return super().setPosition(x, y, z)

    def setRotationX(self, angle):
        self.computeViewMatrix()
        return super().setRotationX(angle)

    def setRotationY(self, angle):
        self.computeViewMatrix()
        return super().setRotationY(angle)

    def setRotationZ(self, angle):
        self.computeViewMatrix()
        return super().setRotationZ(angle)

    def getProjectionMatrix(self):
        return self.getRotationMatrix().dot(self.projection)

    def setTarget(self, target):
        self.target = target
        self.computeViewMatrix()