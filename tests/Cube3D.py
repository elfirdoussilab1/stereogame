from __future__ import division
import pygame
from pygame.locals import *
from geometry import *
from interlacer import Interlacer
from OpenGL.GLU import *
from pyparsing import anyCloseTag


#
#!/usr/bin/env python
from OpenGL.GL import *
import numpy as np
import math
import pygame
from pygame.math import Vector3


#local imports
from geometry import *

with open('./shaders/fbo/fboVertex.glsl', 'r') as file:
    vs_tx = file.read()

with open('./shaders/fbo/fboFragment.glsl', 'r') as file:
    fs_tx = file.read()

with open('./shaders/fbo/flatFragment.glsl', 'r') as file:
    fs_flat = file.read()

with open('./shaders/interlaceVertex.glsl', 'r') as file:
	interlaceVertex = file.read()

with open('./shaders/interlaceFloatFragment.glsl', 'r') as file:
	interlaceFragment = file.read()
#


verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (1,1,1),
    (0,1,1),
    )

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

"""
def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()
"""

def Color():
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x+=1
            glColor3fv(colors[x])
            glVertex3fv(verticies[vertex])
    glEnd()


def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()



def main():
    pygame.init()
    width, height = 1920, 1080
    display = (width,height)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    screen = Rectangle('screen', True)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -5)
    angle = 0
    color = False


    '''perspective_mx = perspective(45, width/height, 0.1, 50)
    model_matrix = np.identity(4, dtype=np.float32)'''
    ortho_mx = ortho(-1, 1, 1, -1, -50, 50)
    ident_matrix = np.identity(4, dtype=np.float32)

    eyeTarget = Vector3(0, 0, 0)

    eye_distance = 0.25

    right_eye = Vector3(-eye_distance / 2, 0, 15)
    right_view_matrix = lookat(right_eye, eyeTarget)

    left_eye = Vector3(eye_distance / 2, 0, 15)
    left_view_matrix = lookat(left_eye, eyeTarget)


    interlacer = Interlacer()

    blackTex = Texture("res/black.jpg")
    textures = [
		blackTex,
		blackTex,
		blackTex,
		blackTex,
		blackTex,
		blackTex,
		blackTex,
		blackTex,
	]

    fbo_width = int(width/2)
    fbo_height = int(height/2)
    
    #create fbo object
    fbo_right = FrameBuffer(fbo_width, fbo_height)
   # fbo_left = FrameBuffer(fbo_width, fbo_height)
    
    '''fbos = [fbo_right, fbo_left]
    view_matrices = [right_view_matrix, left_view_matrix]'''


    def renderView(view_matrix):
            glViewport(0, 0, fbo_width, fbo_height)

            glClearColor(0.0, 0.0, 0.2, 1.0)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glEnable(GL_DEPTH_TEST)
            glEnable(GL_BLEND)



    while True:
        '''for i in range(2):
            fbos[i].bind()
            renderView(view_matrices[i])'''

        fbo_right.bind()
        renderView(right_view_matrix)

        glUseProgram(0)
        #render to main video output
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_BLEND)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glViewport(0, 0, width, height)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        interlacer.use(ortho_mx, ident_matrix)
	    #interlacer.setTextureFromFBO(fbo_left, 0)
        interlacer.setTextureFromFBO(fbo_right, 0)
        for i in range(1, len(textures)):
            textures[i].activate(interlacer.sTextures[i], i)

        screen.draw(interlacer.program)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == KEYDOWN: #fleche gauche augmente angle de rotation, droite diminue
                if event.key == K_LEFT:
                    angle += 1
                elif event.key == K_RIGHT:
                    angle -= 1

            if event.type == MOUSEBUTTONDOWN: #clique souris colore le cube
                if color :
                    color = False
                else :
                    color = True

                    

        glRotatef(angle, 3, 1, 1) #(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        if color : 
            Color()
        Cube()

        pygame.display.flip()
        pygame.time.wait(10)


main()