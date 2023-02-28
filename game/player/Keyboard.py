from game.player.Input import Input
import pygame

class Keyboard(Input):
    def __init__(self):
        self.buttons = None
        self.before = self.buttons # the state of keys before modification
        self.buttons = pygame.key.get_pressed()
        

    def update(self):
        self.before = self.buttons
        self.buttons = pygame.key.get_pressed()

    def isBattePressed(self):
        
        bool = self.buttons[pygame.K_SPACE] and (not self.before[pygame.K_SPACE])
        return bool

    def getEffectButton(self, effect):
        if effect == "batte":
            return self.buttons[pygame.K_SPACE] and (not self.before[pygame.K_SPACE])
        elif effect == "explosion":
            return self.buttons[pygame.K_z] and (not self.before[pygame.K_z])

