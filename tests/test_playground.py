import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from pyparsing import anyCloseTag

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


def main():

    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    program = Program(vs_tx, fs_tx)
    playground = Rectangle('playground')
    playground.setPosition(10, 10, 10)
    playground.setScaling(1, 1, 1)
    playground.draw(program.program)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                playground.getMatrix().dot(rotate(1, 0, 1, 0))

        #glRotatef(angle, 3, 1, 1) #(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        playground.draw(program.program)

        pygame.display.flip()
        pygame.time.wait(10)


main()