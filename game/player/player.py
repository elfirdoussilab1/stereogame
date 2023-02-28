import math

from feather.transform import Transform
from feather.collisions.sphereToCylinder import sphereToCylinder
from feather.algebra import rotate
from game.player.GamePad import GamePad
from game.player.eye import Eye
from pygame.math import Vector3
from game.bat import Bat
import numpy as np
from random import random
import pygame


class Player(Transform):
    def __init__(self, flip, Ztargetting, gamepad, scene, ballManager):
        Transform.__init__(self)
        self.batte = Bat("./assets/baseball/batB.obj", scene)

        self.defaultEyeDistance = 0.09
        self.eyeDistance = self.defaultEyeDistance
        self.Ztargetting=Ztargetting 

        self.leftEye = Eye()  ### Initialiser l'oeil gauche ici
        self.leftEye.setPosition(-self.eyeDistance / 2, 0, 0)

        self.rightEye = Eye()  ### Initialiser l'oeil droit ici
        self.rightEye.setPosition(self.eyeDistance / 2, 0, 0)

        if not flip:
            self.leftEye.setPosition(-self.eyeDistance / 2, 0, 0)
            self.rightEye.setPosition(self.eyeDistance / 2, 0, 0)
        else:
            self.leftEye.setPosition(self.eyeDistance / 2, 0, 0)
            self.rightEye.setPosition(-self.eyeDistance / 2, 0, 0)

        self.flip = flip

        self.setEyesTarget(0, 0, 0)

        self.gamepad = gamepad
        self.invincible = False
        self.state = 0

        self.isZTargeting = False

        self.score = 0

        self.ballManager = ballManager

    def getGamepad(self):
        return self.gamepad

    def setinvincible(self, invincible):
        self.invincible = invincible

    def reverseView(self):
        self.rightEye, self.leftEye = self.leftEye, self.rightEye

    # def setFOV(self, fov):
    #    self.oeilDroit.fov = fov
    #    self.oeilGauche.fov = fov

    def setRotationX(self, angle):

        self.rightEye.setPosition(-self.eyeDistance / 2, 0, 0)
        self.rightEye.setRotationX(angle)
        self.rightEye.setRotationXAround(angle, self.position.x, self.position.y, self.position.z)
        self.rightEye.computeViewMatrix()

        self.leftEye.setPosition(self.eyeDistance / 2, 0, 0)
        self.leftEye.setRotationX(angle)
        self.leftEye.setRotationXAround(angle, self.position.x, self.position.y, self.position.z)
        self.leftEye.computeViewMatrix()

        super().setRotationX(angle)

    def setRotationY(self, angle):
        self.rightEye.setPosition(-self.eyeDistance / 2, 0, 0)
        self.rightEye.setRotationY(angle)
        self.rightEye.setRotationYAround(angle, self.position.x, self.position.y, self.position.z)
        self.rightEye.computeViewMatrix()

        self.leftEye.setPosition(self.eyeDistance / 2, 0, 0)
        self.leftEye.setRotationY(angle)
        self.leftEye.setRotationYAround(angle, self.position.x, self.position.y, self.position.z)
        self.leftEye.computeViewMatrix()

        super().setRotationY(angle)

    def setRotationZ(self, angle):
        self.rightEye.setPosition(-self.eyeDistance / 2, 0, 0)
        self.rightEye.setRotationZ(angle)
        self.rightEye.setRotationZAround(angle, self.position.x, self.position.y, self.position.z)
        self.rightEye.computeViewMatrix()

        self.leftEye.setPosition(self.eyeDistance / 2, 0, 0)
        self.leftEye.setRotationZ(angle)
        self.leftEye.setRotationZAround(angle, self.position.x, self.position.y, self.position.z)
        self.leftEye.computeViewMatrix()

        super().setRotationZ(angle)

    def setPosition(self, x, y, z):
        self.rightEye.setPosition(x - self.eyeDistance / 2, y, z)
        self.leftEye.setPosition(x + self.eyeDistance / 2, y, z)
        self.batte.setPosition(x, y, z)
        if self.flip:
            self.batte.beginY = -30
            self.batte.endY = 40
            self.batte.beginZ = 50
            self.batte.endZ = 50
            self.batte.setRotationZ(self.batte.beginZ)
            self.batte.setRotationY(self.batte.beginY)
        else:
            self.batte.beginY = 30
            self.batte.endY = -40
            self.batte.beginZ = 180 - 50
            self.batte.endZ = 180 - 50
            self.batte.setRotationZ(self.batte.beginZ)
            self.batte.setRotationY(self.batte.beginY)

        return super().setPosition(x, y, z)

    def increaseEyeDistance(self, amount: float):
        self.eyeDistance += amount
        self.setEyeDistance(self.eyeDistance)

    def decreaseEyeDistance(self, amount: float):
        self.eyeDistance -= amount
        self.setEyeDistance(self.eyeDistance)

    def setEyesTarget(self, x, y, z):
        self.rightEye.setTarget(Vector3(x, y, z))
        self.leftEye.setTarget(Vector3(x, y, z))

    def setEyeDistance(self, eyeDistance: float):
        self.eyeDistance = eyeDistance
        if not self.flip:
            self.rightEye.setPosition(self.position.x - self.eyeDistance / 2, self.position.y, self.position.z)
            self.leftEye.setPosition(self.position.x + self.eyeDistance / 2, self.position.y, self.position.z)
        else:
            self.rightEye.setPosition(self.position.x + self.eyeDistance / 2, self.position.y, self.position.z)
            self.leftEye.setPosition(self.position.x - self.eyeDistance / 2, self.position.y, self.position.z)

    def invertEyes(self):
        self.rightEye, self.leftEye = self.leftEye, self.rightEye

    def update(self, deltaTime: float):
        self.batte.update(deltaTime)

        relativePosition1 = np.array([-1.0, -6.0, 0.0])
        relativePosition2 = np.array([-6.0, -2.0, 0.0])

        if self.batte.isSuperBat:
            relativePosition1 *= 1.5
            relativePosition2 *= 1.5
            self.batte.setScaling(0.8, 0.8, 0.8)
        else:
            self.batte.setScaling(0.7, 0.7, 0.7)

        relativePosition1 = self.batte.getRotationMatrix().dot(
            np.array([relativePosition1[0], relativePosition1[1], relativePosition1[2], 1.0]))
        relativePosition1 = np.array([relativePosition1[0], relativePosition1[1], relativePosition1[2]])

        flipedRotationMatrix = rotate(self.batte.rotation.x, 1.0, 0.0, 0.0)
        flipedRotationMatrix = flipedRotationMatrix.dot(rotate(self.batte.rotation.y, 0.0 , 1.0, 0.0))
        flipedRotationMatrix = flipedRotationMatrix.dot(rotate(-self.batte.rotation.z, 0.0, 0.0, 1.0))

        relativePosition2 = flipedRotationMatrix.dot(
            np.array([relativePosition2[0], relativePosition2[1], relativePosition2[2], 1.0]))
        relativePosition2 = np.array([relativePosition2[0], relativePosition2[1], relativePosition2[2]])

        if not self.flip:
            self.batte.end1 = relativePosition1 + np.array([self.position.x, self.position.y, self.position.z])
        else:
            self.batte.end1 = relativePosition2 + np.array([self.position.x, self.position.y, self.position.z])

        if not self.flip:
            self.batte.end1[2] -= 4.5
            self.batte.end2 = np.array(
                [self.getPosition().x, self.getPosition().y, self.getPosition().z - 4.5])
        else:
            self.batte.end1[2] += 4.5
            self.batte.end2 = np.array(
                [self.getPosition().x, self.getPosition().y, self.getPosition().z + 4.5])

        for ball in self.ballManager.balls:
            if sphereToCylinder(ball, self.batte):
                strike_sound = pygame.mixer.Sound("./assets/strike.mp3")
                pygame.mixer.Sound.play(strike_sound)

                zInfluence = 1.5

                velocity = np.array([-ball.velocity.x, -ball.velocity.y, -ball.velocity.z * zInfluence])
                velocityNorm = math.sqrt(velocity[0] ** 2 + velocity[1] ** 2 + velocity[2] ** 2)

                velocity /= velocityNorm
                velocity *= 0.2

                if self.flip:
                    if not self.isZTargeting:
                        ball.setVelocity(-velocity[0] + (random() - 0.5) / 10, -velocity[1] + (random() - 0.5) / 10, -abs(velocity[2]))
                    else:
                        ball.setVelocity(0, 0, -abs(velocity[2]))
                else:   
                    if not self.isZTargeting:
                        ball.setVelocity(-velocity[0] + (random() - 0.5) / 10, -velocity[1] + (random() - 0.5) / 10, abs(velocity[2]))
                    else:
                        ball.setVelocity(0, 0, abs(velocity[2]))
                ball.currentPlayer = self