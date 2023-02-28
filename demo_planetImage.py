from OpenGL.GL import *
import numpy as np
import pygame

#local imports
from feather import Texture, Screen
from feather.shapes import Rectangle
from feather.projections import *
from feather.algebra import *
from interlacer import Interlacer

if __name__ == "__main__":
	width, height = 1920, 1080
	pygame.init()
	pygame.display.set_mode((width, height), pygame.DOUBLEBUF|pygame.OPENGL|pygame.HWSURFACE, 0)
	pygame.display.toggle_fullscreen()

	rect = Rectangle('rect', False)
	screen = Screen('screen')

	#create matrices
	ortho_mx = ortho(-1, 1, 1, -1, -50, 50)
	ident_matrix = np.identity(4, dtype=np.float32)

	interlaceProgram = Interlacer()

	blackTex = Texture("./assets/black.jpg")

	textures = [
		Texture("./assets/planet/planet_droite.png"),
		Texture("./assets/planet/planet_gauche.png"),
		blackTex,
		blackTex,
		blackTex,
		blackTex,
		blackTex,
		blackTex,
	]
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

	glViewport(0, 0, width, height)

	running = True
	while running:
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		
		interlaceProgram.use(ortho_mx, ident_matrix)
		for i in range(len(textures)):
			interlaceProgram.setTextureFromImage(textures[i], i)

		screen.draw(interlaceProgram.program)

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