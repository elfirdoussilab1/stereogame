from feather.materials.textureMaterial import TextureMaterial
from feather.shapes import Sphere, Rectangle
from feather.algebra import reflection
import numpy as np
from feather.collisions.sphereToCylinder import sphereToCylinder
import pygame
from random import random

from feather.texture import Texture
from feather.vector3 import Vec3

class Projectile(Sphere):
        def __init__(self, name, flip,  radius, battlefield, collision, ballmanager, scene):
            Sphere.__init__(self, name, flip, scene)
            self.collision = collision  # if it is equal to reflect, then it will reflect
                                        # and if it is equal to teleport than we will apply the function teleport
            self.position = Vec3(0.0, 0.0, 0.0)
            self.velocity = Vec3(0.0, 0.0, 0.0)
            self.acceleration = Vec3(0.0, 0.0, 0.0)
            self.radius = radius
            self.battlefield = battlefield
            ballmanager.addBall(self)
            self.ballmanager = ballmanager
            
            self.setScaling(radius, radius, radius)
            self.currentPlayer = None
            self.scene.addShape(self)

        def setCurrentPlayer(self,player):
            self.currentPlayer = player


        def update(self, deltaTime):
            player1 = self.battlefield.player1
            player2 = self.battlefield.player2
            comptSwitch = 0
            comptSuper1 = 0
            comptSuper2 = 0
            comptEye1 = 0
            comptEye2 = 0
            r = self.getRadius()
            position = self.getPosition()
            x,y,z = position.x, position.y, position.z
            sizex,sizey,sizez = self.battlefield.getSizex(), self.battlefield.getSizey(), self.battlefield.getSizez()
            

            ## maintenant s'il y a collision avec les murs

            if self.battlefield.isCollision(r, position):
                where = self.battlefield.whereCollision(r, position)

                ## scoring a goal with normal ball

                if self.collision == 'reflect':
                    if where == 'front':
                        self.ballmanager.removeBall(self)
                        if player1.position.z > 0: # player 1 wins
                            player1.score+=1
                            
                        if player1.position.z < 0: # player 2 wins
                            player2.score+=1
                            
                    elif where == 'back':
                        self.ballmanager.removeBall(self)
                        if player1.position.z < 0: # player 1 wins
                            player1.score+=1
                            
                        if player1.position.z > 0: # player 2 wins
                            player2.score+=1
                            
            
                    else:
                        normVect = self.battlefield.normalVector(where)
                        oldVelocity = self.getVelocity()
                        newVelocity = reflection(oldVelocity, normVect)

                        self.setVelocity(newVelocity.x, newVelocity.y, newVelocity.z)

                ### teleport effect

                if self.collision == 'teleport':
                    if where == 'front':
                        self.ballmanager.removeBall(self)
                        if player1.position.z > 0: # player 1 wins
                            player1.score+=1
                            
                        elif player1.position.z < 0: # player 2 wins
                            player2.score+=1
                            
                    elif where == 'back':
                        self.ballmanager.removeBall(self)
                        if player1.position.z < 0: # player 1 wins
                            player1.score+=1
                            
                        if player1.position.z > 0: # player 2 wins
                            player2.score+=1
                            
                    
                    elif where == 'right':
                        self.setPosition(x-2*sizex+2*r + 0.1, y, z)
                    elif where == 'left':
                        self.setPosition(x+2*sizex-2*r-0.1, y, z)
                    elif where == 'top':
                        self.setPosition(x, y - 2*sizey + 2*r - 0.1, z)
                    elif where == 'bottom':
                        self.setPosition(x, y + 2*sizey - 2*r + 0.1, z)
                
                ## bomb explosion with front and back face

                if self.collision == 'bomb':
                    if where == 'front':
                        self.explode()
                        if player1.position.z > 0: # player 2 wins
                            player2.score+=1
                        if player1.position.z < 0: # player 1 wins
                            player1.score+=1
                            
                    if where == 'back':
                        self.explode()
                        if player1.position.z < 0: # player 2 wins
                            player2.score+=1
                        if player1.position.z > 0: # player 1 wins
                            player1.score+=1
            
                    
                    else:
                        normVect = self.battlefield.normalVector(where)
                        oldVelocity = self.getVelocity()
                        newVelocity = reflection(oldVelocity, normVect)

                        self.setVelocity(newVelocity.x, newVelocity.y, newVelocity.z)
            
            # si collision avec une batte et que c'est une bombe
            
            if self.collision == 'bomb': 
                if sphereToCylinder(self, player1.batte):
                    self.explode()
                    player2.score+=1
                if sphereToCylinder(self,player2.batte):
                    self.explode()
                    player2.score+=1

            ## superbat effect
            if player1.batte.isSuperBat:
                comptSuper1 += deltaTime
                if comptSuper1 >= 3:
                    player1.batte.isSuperBat = False
                    comptSuper1 = 0

            if player2.batte.isSuperBat:
                comptSuper2 += deltaTime
                if comptSuper2 >= 3:
                    player2.batte.isSuperBat = False
                    comptSuper2 = 0

            #### increasing eye distance effect

            if player1.eyeDistance > player1.defaultEyeDistance:
                # we applied the effect of increasing the eye distance
                comptEye1 += deltaTime
                if comptEye1 >=3:
                    player1.eyeDistance = player1.defaultEyeDistance
                    comptEye1 = 0
            if player2.eyeDistance > player2.defaultEyeDistance:
                # we applied the effect of increasing the eye distance
                comptEye2 += deltaTime
                if comptEye2 >=3:
                    player2.eyeDistance = player2.defaultEyeDistance
                    comptEye2 = 0
            
            #### decreasing eye distance effect

            if player1.eyeDistance < player1.defaultEyeDistance:
                # we applied the effect of increasing the eye distance
                comptEye1 += deltaTime
                if comptEye1 >=3:
                    player1.eyeDistance = player1.defaultEyeDistance
                    comptEye1 = 0

            if player2.eyeDistance < player2.defaultEyeDistance:
                # we applied the effect of increasing the eye distance
                comptEye2 += deltaTime
                if comptEye2 >=3:
                    player2.eyeDistance = player2.defaultEyeDistance
                    comptEye2 = 0

            #### switch views effect

            if self.battlefield.areViewsSwitched:
                comptSwitch += deltaTime
                if comptSwitch >= 3:
                    self.battlefield.areViewsSwitched = False


            self.translate(self.velocity.x, self.velocity.y, self.velocity.z)
            newVelocity = Vec3(self.velocity.x+self.acceleration.x, self.velocity.y+self.acceleration.y, self.velocity.z+self.acceleration.z)
            self.velocity = newVelocity
            
        def setVelocity(self, x, y, z):
           self.velocity = Vec3(x, y, z)

        def getVelocity(self):
            return self.velocity

        def setAcceleration(self, x, y, z):
            self.acceleration = Vec3(x, y, z)

        def getAcceleration(self):
            return self.acceleration

        def getRadius(self):
            return self.radius

        def getEnds(self):
            futurePosition = np.array([self.position.x+self.velocity.x, self.position.y+self.velocity.y, self.position.z+self.velocity.z])
            ends = np.add(self.vertices, np.full((len(self.vertices), 3), futurePosition))
            return ends

        def setCollision(self, collision):
            self.collision = collision
        
        def showTrajectory(self):
            traj = Rectangle('traj', False, self.scene)
            traj.setPosition(self.position.x, self.position.y, self.position.z)
            traj.setScaling(0.5, 0.005, 1)

        def applyEffect(self, effect):
            if effect == 'disparition':
                #ballMat = TextureMaterial(Texture("./assets/texBattle.jpeg"))
                self.setMaterial(self.battlefield.material)
                #self.update()

            elif effect == 'teleport':
                ballMat = TextureMaterial(Texture("./assets/Galaxy512.jpg"))
                self.setMaterial(ballMat)
                self.setCollision('teleport')
                #self.update()

            elif effect == 'bomb':
                self.setCollision('bomb')
                bombMat = TextureMaterial(Texture("./assets/explosion.png"))
                self.setMaterial(bombMat)
                #self.update()

            elif effect == 'x3':
                position = self.getPosition()
                x,y,z = position.x, position.y, position.z
                proj1 = Projectile("sphery", False, 1, self.battlefield, 'reflect',self.ballmanager, self.scene)
                proj2 = Projectile("sphery", False, 1, self.battlefield, 'reflect',self.ballmanager, self.scene)
                ballMat = TextureMaterial(Texture("./assets/basketball.jpeg"))
                proj1.setMaterial(ballMat)
                proj2.setMaterial(ballMat)
                proj1.setPosition(x,y,z)
                proj2.setPosition(x,y,z)
                proj1.setVelocity((random() - 0.5) / 2.0, (random() - 0.5) / 2.0, (random() - 0.5) / 2.0)
                proj2.setVelocity((random() - 0.5) / 2.0, (random() - 0.5) / 2.0, (random() - 0.5) / 2.0)
                proj1.ballmanager.addBall(proj1)
                proj2.ballmanager.addBall(proj2)

            elif effect == 'superbat':
                if self.currentPlayer != None:
                    self.currentPlayer.batte.isSuperBat = True

            elif effect == 'increaseEyeDistance':
                if self.currentPlayer != None:
                    if self.currentPlayer == self.battlefield.player1:
                        self.battlefield.player2.increaseEyeDistance(0.1)
                    else:
                        self.battlefield.player1.increaseEyeDistance(0.1)

            elif effect == 'deceaseEyeDistance':
                if self.currentPlayer != None:
                    if self.currentPlayer == self.battlefield.player1:
                        self.battlefield.player2.decreaseEyeDistance(0.1)
                    else:
                        self.battlefield.player1.decreaseEyeDistance(0.1)
            elif effect == 'switchViews':
                self.battlefield.areViewsSwitched = True

        def explode(self):
            crash_sound = pygame.mixer.Sound("./assets/boomSound.mp3")
            pygame.mixer.Sound.play(crash_sound)
            self.ballmanager.removeBall(self)