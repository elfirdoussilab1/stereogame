from __future__ import division
import pygame, numpy
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.GLU import *
from OpenGL.arrays import vbo

pygame.init()
pygame.display.set_mode((1920, 1080), DOUBLEBUF | OPENGL)


# Generate a texture
img = pygame.font.Font(None, 200).render("Start", True, (200, 30, 30), (0,20,20))
w, h = img.get_size()
texture = glGenTextures(1)
glPixelStorei(GL_UNPACK_ALIGNMENT,1)
glBindTexture(GL_TEXTURE_2D, texture)
glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
data = pygame.image.tostring(img, "RGBA", 1)
glTexImage2D(GL_TEXTURE_2D, 0, 4, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)


show = True
clock = pygame.time.Clock()
while show:
        dt = 0.001 * clock.tick(40)
        for event in pygame.event.get():
                if event.type in (MOUSEBUTTONDOWN, KEYDOWN, QUIT):
                        playing = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)



        # Display texture
        glBindTexture(GL_TEXTURE_2D, texture)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glTranslate(-1, -1, 0)
        glScale(2 / 600, 2 / 400, 1)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        glDisable(GL_LIGHTING)
        glBegin(GL_QUADS)
        x0, y0 = 100, 100
        w, h = img.get_size()
        for dx, dy in [(0, 0), (0, 1), (1, 1), (1, 0)]:
                glVertex(x0 + dx * w, y0 + dy * h, 0)
                glTexCoord(dy, 1 - dx)
        glEnd()


        pygame.display.flip()