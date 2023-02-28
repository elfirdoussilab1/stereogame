#!/usr/bin/env python
from __future__ import division
from OpenGL.GL import *
import numpy as np
import math
import pygame


#local imports
from geometry import *

vs_dual_tx = textwrap.dedent("""\
    uniform mat4 uMVMatrix;
    uniform mat4 uPMatrix;
       
    attribute vec3 aVertex;
    attribute vec2 aTexCoord;
    
    varying vec2 vTexCoord;
    
    void main(){
       vTexCoord = aTexCoord;
       gl_Position = (uPMatrix * uMVMatrix)  * vec4(aVertex, 1.0);
    }
    """)

fs_dual_tx = textwrap.dedent("""\
    uniform sampler2D sTexture1;
    uniform sampler2D sTexture2;

    varying vec2 vTexCoord;

    void main() {
       	if (int( mod(gl_FragCoord.x, 2.0) ) == 1) {
           gl_FragColor = texture2D(sTexture1, vec2(vTexCoord.x, vTexCoord.y) );
		} else {
           gl_FragColor = texture2D(sTexture2, vec2(vTexCoord.x, vTexCoord.y) );
		}
    }
    """)


if __name__ == "__main__":
	width, height = 1920, 1080
	pygame.init()
	pygame.display.set_mode((width, height), pygame.DOUBLEBUF|pygame.OPENGL|pygame.HWSURFACE, 0)
	pygame.display.toggle_fullscreen()

	rect = Rectangle('rect')
	rect_flip = Rectangle('rect_flip', True)

	#create matrices
	ortho_mx = ortho(-1, 1, 1, -1, -50, 50)
	ident_matrix = np.identity(4, dtype=np.float32)

	prog1 = Program(vs_dual_tx, fs_dual_tx)
	sTexture1 = prog1.getUniformLocation("sTexture1")
	sTexture2 = prog1.getUniformLocation("sTexture2")

	texture1 = Texture("../assets/Galaxy.jpg")
	texture2 = Texture("../assets/tennis.png")


	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

	glViewport(0, 0, width, height)

	running = True
	while running:

		#draw final view interleave, draw full-screen quad with all our textures
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		prog1.use(ortho_mx, ident_matrix)

		texture2.activate(sTexture2, 1)
		texture1.activate(sTexture1, 0)

		rect_flip.draw(prog1.program)

		pygame.display.flip()

		events = pygame.event.get()
		if len(events):
			for event in events:
				if event.type == pygame.QUIT:
					running = False
				if event.type == pygame.MOUSEMOTION:
					x, y = event.rel
					if any(event.buttons):
						model_matrix = model_matrix.dot(rotate(y, -1, 0, 0)).dot(rotate(x, 0, -1, 0))

