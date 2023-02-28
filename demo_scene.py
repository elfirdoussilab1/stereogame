from OpenGL.GL import *
import numpy as np
import pygame
from pygame.math import Vector3

#local imports
from feather import Texture, FrameBuffer, Scene, Screen, Camera
from feather.shapes import Rectangle, Cube
from feather.materials import ColorMaterial, TextureMaterial
from feather.projections import *
from feather.algebra import *
from interlacer import Interlacer

if __name__ == "__main__":
	width, height = 1920, 1080
	pygame.init()
	pygame.display.set_mode((width, height), pygame.DOUBLEBUF|pygame.OPENGL|pygame.HWSURFACE, 0)
	pygame.display.toggle_fullscreen()

	scene = Scene()
	
	# shapes
	rect = Rectangle('rect', False, scene)
	rect.setPosition(-6, -3, 0)
	rect.setScaling(0.5, 0.5, 1)
	rectMat = ColorMaterial(1.0, 0.0, 0.0)
	rect.setMaterial(rectMat)

	rect2 = Rectangle('rect2', False, scene)
	z_position_rect = 0
	rect2.setPosition(6, 3, z_position_rect)
	rect2.setScaling(0.5, 0.5, 1)

	rect2Mat = ColorMaterial(0.0, 1.0, 0.0)
	rect2.setMaterial(rect2Mat)

	yellow_cube = Cube('yellow_cube', True, scene)
	yellow_cube.setScaling(0.5, 0.5, 0.5)
	yellow_cube.setRotationY(45)
	
	cubeMat = TextureMaterial(Texture("./assets/tennis.png"))
	yellow_cube.setMaterial(cubeMat)

	galaxy_rect = Rectangle('galaxy_rect', True, scene)
	galaxy_rect.setPosition(0, 0, -6)
	galaxy_rect.setScaling(8 * width / height, 8, 1)

	galaxyMat = TextureMaterial(Texture("./assets/Galaxy.jpg"))
	galaxy_rect.setMaterial(galaxyMat)
	
	# screen
	screen = Screen('screen')

	# create matrices

	rightCamera = Camera(45, width / height)
	leftCamera = Camera(45, width / height)

	model_matrix = np.identity(4, dtype=np.float32)
	ortho_mx = ortho(-1, 1, 1, -1, -50, 50)
	ident_matrix = np.identity(4, dtype=np.float32)

	eye_distance = 0.008

	rightCamera.setPosition(-eye_distance / 2, 0, 5)
	leftCamera.setPosition(eye_distance / 2, 0, 5)

	interlacer = Interlacer()

	blackTex = Texture("./assets/black.jpg")

	fbo_width = int(width/2)
	fbo_height = int(height/2)
	
	#create fbo object
	fbo_right = FrameBuffer(fbo_width, fbo_height)
	fbo_left = FrameBuffer(fbo_width, fbo_height)

	fbos = [fbo_right, fbo_left]
	cameras = [rightCamera, leftCamera]

	getTicksLastFrame = 0.0
	x,z = 0.0, 0.0
	circleRadius = 1.7

	running = True
	while running:
		time = pygame.time.get_ticks() / 1000.0
		deltaTime = time - getTicksLastFrame
		getTicksLastFrame = time
		
		yellow_cube.setRotationY(45.0 + time * 50.0)
		yellow_cube.setRotationX(60.0 * time)

		#rightCamera.setRotationY(time * 50)
		#leftCamera.setRotationY(time * 50)

		rotationSpeed = 1
		x = math.cos(time * rotationSpeed) * circleRadius
		z = math.sin(time * rotationSpeed) * circleRadius

		yellow_cube.setPosition(x, 0, z)

		for i in range(2):
			fbos[i].bind()
			glViewport(0, 0, fbo_width, fbo_height)
			if i == 0 or i == 1:
				rect.material.color = (1.0, 0.0, 0.0)
			elif i == 4 or i == 5:
				rect.material.color = (0.0, 1.0, 0.0)
			else:
				rect.material.color = (0.0, 0.0, 1.0)
			scene.render(cameras[i].getProjectionMatrix(), model_matrix, cameras[i].computeViewMatrix())

		glUseProgram(0)
		#render to main video output
		glBindFramebuffer(GL_FRAMEBUFFER, 0)
		glDisable(GL_DEPTH_TEST)
		glDisable(GL_BLEND)

		glClearColor(0.0, 0.0, 0.0, 1.0)
		glViewport(0, 0, width, height)
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		### drawing on screen
		interlacer.use(ortho_mx, ident_matrix)

		interlacer.setTextureFromFBO(fbo_left, 0)
		interlacer.setTextureFromFBO(fbo_right, 1)
		interlacer.setTextureFromImage(blackTex, 2)
		interlacer.setTextureFromImage(blackTex, 3)
		interlacer.setTextureFromImage(blackTex, 4)
		interlacer.setTextureFromImage(blackTex, 5)
		interlacer.setTextureFromImage(blackTex, 6)
		interlacer.setTextureFromImage(blackTex, 7)

		screen.draw(interlacer.program)

		pygame.display.flip()

		keys = pygame.key.get_pressed()
		if keys[pygame.K_z]:
			circleRadius += 0.05
		if keys[pygame.K_s]:
			circleRadius -= 0.05
			print("Eye distance : ", eye_distance)
		if keys[pygame.K_UP]:
			eye_distance += 0.001
			print("Eye distance : ", eye_distance)
		if keys[pygame.K_DOWN] :
			eye_distance -= 0.001
		if keys[pygame.K_RIGHT] :
			z_position_rect += 0.01
			rect2.setPosition(6, 3, z_position_rect)
			print("z_position_rect : ", z_position_rect)
		if keys[pygame.K_LEFT] :
			z_position_rect -= 0.01
			rect2.setPosition(6, 3, z_position_rect)
			print("z_position_rect : ", z_position_rect)
		if keys[pygame.K_g] :
			rightCamera.setTarget(Vector3(eye_distance / 2, 0, 0))
		if keys[pygame.K_d] :
			rightCamera.setTarget(Vector3(-eye_distance / 2, 0, 0))
		if keys[pygame.K_f] :
			rightCamera.setTarget(Vector3(0, 0, 0))

		
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEMOTION:
				x, y = event.rel
				if any(event.buttons):
					model_matrix = model_matrix.dot(rotate(y, -1, 0, 0)).dot(rotate(x, 0, -1, 0))