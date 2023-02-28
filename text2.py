from __future__ import division
import pygame
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()
pygame.display.set_mode((1920, 1080), DOUBLEBUF | OPENGL)

def drawText(position, textString):     
    font = pygame.font.Font (None, 300)
    textSurface = font.render(textString, True, (255,0,50), (0,20,20))     
    textData = pygame.image.tostring(textSurface, "RGBA", True)     
    glRasterPos3d(*position)     
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

show = True
clock = pygame.time.Clock()
while show:
        dt = 0.001 * clock.tick(40)
        for event in pygame.event.get():
                if event.type in (MOUSEBUTTONDOWN, KEYDOWN, QUIT):
                        show = False

        # Display texture
        drawText([-0.25, 1, 0], " Start ")
        pygame.display.flip()
