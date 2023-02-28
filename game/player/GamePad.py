import pygame
from game.player.Input import Input
from random import random
buttons = {'TRIANGLE':0,'ROUND':1,'X':2,'SQUARE':3,'L1':4,'R1':5,'L2':6,'R2':7,'SELECT':8,'START':9,'JOY1':10,'JOY2':11,'ANALOG':12}
class GamePad(Input):
    
    # initializing all buttons states to False
    def __init__(self,id):
        self.id = id
        self.stateBefore = None # the state of keys before modification
        n = pygame.joystick.Joystick(id).get_numbuttons()
        print("the number of buttons is " + str(n))
        self.stateButtons = []
        for i in range(n):
            self.stateButtons.append(False)
        
        

    def update(self):
        self.stateBefore = list(self.stateButtons)
        n = len(self.stateButtons)
        for i in range(n):
            self.stateButtons[i] = pygame.joystick.Joystick(self.id).get_button(i)
        
    def isBattePressed(self):
        return self.stateButtons[buttons['ROUND']]
    
    def turnBatteLeft(self) :
        return self.stateButtons[buttons['L1']] or self.stateButtons[buttons['L2']]

    def turnBatteRight(self) :
        return self.stateButtons[buttons['R1']] or self.stateButtons[buttons['R2']]

    def startButton(self) :
        return self.stateButtons[buttons['START']]

    """def getEffectButton(self, effect):
        if effect == "batte":
            return self.stateButtons[buttons['SQUARE']] and (not self.stateBefore[buttons['SQUARE']])
        elif effect == "explosion":
            return self.stateButtons[buttons['X']] and (not self.stateBefore[buttons['X']])"""

    def getZtargetting(self):
        return self.stateButtons[buttons['X']]

