from OpenGL.GL import *
import numpy as np
import pygame
from Bomb import Bomb

#local imports
from geometry import *

vs_tx = textwrap.dedent("""\
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

fs_tx = textwrap.dedent("""\
    uniform sampler2D sTexture;

    varying vec2 vTexCoord;

    void main() {
	   gl_FragColor = texture2D(sTexture, vTexCoord);
    }
    """)

fs_flat = textwrap.dedent("""\
	uniform vec4 col;
    void main() {
       gl_FragColor = col;
    }
    """)

if __name__ == "__main__":
	width, height = 1920, 1080
	pygame.init()
	pygame.display.set_mode((width, height), pygame.DOUBLEBUF|pygame.OPENGL|pygame.HWSURFACE, 0)
	rect = Rectangle('rect')
	rect_flip = Rectangle('rect_flip', True)

	#create matrices

	perspective_mx = perspective(45, width/height, 0.1, 100)
	model_matrix = np.identity(4, dtype=np.float32)

	eye = pygame.math.Vector3(0, 0, 10)
	center = pygame.math.Vector3(0, 0, 0)
	view_matrix = lookat(eye, center)


	prog1 = Program(vs_tx, fs_tx)
	sTexture1 = prog1.getUniformLocation("sTexture")
	texture1 = Texture("../assets/Galaxy.jpg")
	texture3 = Texture("../assets/tennis.png")
	prog2 = Program(vs_tx, fs_flat)
	uCol = prog2.getUniformLocation("col")
	prog3 = Program(vs_tx, fs_tx)
	sTexture3 = prog3.getUniformLocation("sTexture")
	glViewport(0, 0, width, height)
	running = True
	while running:
		eyemx = view_matrix

		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glEnable(GL_DEPTH_TEST)
		glEnable(GL_BLEND)

		mv_matrix = translate(0, 0, -4).dot(scale(2*width/height, 2, 1)).dot(model_matrix).dot(eyemx)
		prog1.use(perspective_mx, mv_matrix)
		texture1.activate(sTexture1)
		#rect_flip.draw(prog2.program)
		texture3.activate(sTexture3)
		mv_matrix = translate(0, 0, -2).dot(model_matrix).dot(eyemx)
		prog1.use(perspective_mx, mv_matrix)
		glUniform4f(uCol, 1, 0, 0, 1)
		texture.activate(sTexture)
		obj.draw(prog1.program, sTexture)
		cube.draw(prog1.program)

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
