from OpenGL.GL import *
from feather.texture import Texture

# object wrapping GLSL program and shader setup
#
# to build program:
# prog = Program(vertex_shader_source, fragment_shader_source)
#
# to use program:
# prog.use(projection_matrix, modelview_matrix)
#
# to query uniform location:
# prog.getUniformLocation(uniName)
#
class Program:
    def __init__(self, vshader_src, fshader_src):
        vertex_shader = self.__load_shader__(GL_VERTEX_SHADER, vshader_src)
        if vertex_shader == 0:
            exit()

        fragment_shader = self.__load_shader__(GL_FRAGMENT_SHADER, fshader_src)
        if fragment_shader == 0:
            exit()

        self.program = glCreateProgram()
        if self.program == 0:
            print('Failed to allocate GL program')
            exit()

        glAttachShader(self.program, vertex_shader)
        glAttachShader(self.program, fragment_shader)
        glLinkProgram(self.program)

        if glGetProgramiv(self.program, GL_LINK_STATUS, None) == GL_FALSE:
            glDeleteProgram(self.program)
            print('Failed to link GL program')
            exit()

        self.u_mv_mx = glGetUniformLocation(self.program, "uMVMatrix")
        self.u_proj_mx = glGetUniformLocation(self.program, "uPMatrix")

    def __load_shader__(self, shader_type, source):
        shader = glCreateShader(shader_type)
        if shader == 0:
            return 0
        glShaderSource(shader, source)
        glCompileShader(shader)
        if glGetShaderiv(shader, GL_COMPILE_STATUS, None) == GL_FALSE:
            info_log = glGetShaderInfoLog(shader)
            print(info_log)
            glDeleteProgram(shader)
            return 0
        return shader

    def use(self, proj_mx, view_mx):
        glUseProgram(self.program)
        glUniformMatrix4fv(self.u_proj_mx, 1, GL_FALSE, proj_mx)
        glUniformMatrix4fv(self.u_mv_mx, 1, GL_FALSE, view_mx)

    def getUniformLocation(self, name: str):
        return glGetUniformLocation(self.program, name)

    def setFloat(self, uniformName: str, x: float):
        glUniform1f(self.getUniformLocation(uniformName), x)

    def setVector3(self, uniformName: str, x: float, y: float, z: float):
        glUniform3f(self.getUniformLocation(uniformName), x, y, z)

    def setVector4(self, uniformName: str, x: float, y: float, z: float, w: float):
        glUniform4f(self.getUniformLocation(uniformName), x, y, z, w)

    def setTexture(self, uniformName: str, texture: Texture):
        texture.activate(self.getUniformLocation(uniformName), 0)
