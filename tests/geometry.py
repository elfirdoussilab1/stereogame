#!/usr/bin/env python
import os
from matplotlib.pyplot import draw 
import numpy as np
from OpenGL.GL import *
import math
import pygame
from PIL import Image
import textwrap

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

    def getUniformLocation(self, name):
        return glGetUniformLocation(self.program, name)

    def setVector3(self, uniformName: str, x: float, y: float, z: float):
        glUniform3f(self.getUniformLocation(uniformName), x, y, z)

    def setVector4(self, uniformName: str, x: float, y: float, z: float, w: float):
        glUniform4f(self.getUniformLocation(uniformName), x, y, z, w)

    def setTexture(self, uniformName: str, texture):
        texture.activate(self.getUniformLocation(uniformName), 0)


# Objct wrapping texture loader from file to GPU
# to build texture:
# tx = Texture(image_file)
#
# to bind texture to uniform
# tx.activate(uniform_tx)
#
# If multiple textures in fragment shader, start from max texture unit to first one, eg:
# tx.activate(uniform_tx2, 1)
# tx.activate(uniform_tx1, 0)
#
class Texture:
    def __init__(self, filename):
        img = Image.open(filename, 'r').convert("RGB")
        img_data = np.array(img, dtype=np.uint8)
        w, h = img.size

        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

    def activate(self, tx_uni_loc, tx_id = 0):
        glActiveTexture(GL_TEXTURE0 + tx_id)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glUniform1i(tx_uni_loc, tx_id)


# Objct wrapping openGL offscreen framebuffer setup
# to build FBO:
# fbo = FrameBuffer(offs_w, offs_h)
#
# to set FBO the current render target:
# fbo.bind()
#
# to bind fbo underlying texture to uniform (same as with texture.activate):
# fbo.bind_texture(uniform_tx)
#
# If multiple textures in fragment shader, start from max texture unit to first one, eg:
# fbo.bind_texture(uniform_tx2, 1)
# fbo.bind_texture(uniform_tx1, 0)
#
class FrameBuffer:
    def __init__(self, width, height):
        self.fbo = GLuint()
        glGenFramebuffers(1, self.fbo)
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        self.fbo_tx = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.fbo_tx)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.fbo_tx, 0)

        rbo = GLuint()
        glGenRenderbuffers(1, rbo)
        glBindRenderbuffer(GL_RENDERBUFFER, rbo)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, width, height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, rbo)

        if not glCheckFramebufferStatus(GL_FRAMEBUFFER) == GL_FRAMEBUFFER_COMPLETE:
            print('framebuffer binding failed')
            exit()
        self.width = width
        self.height = height

    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)

    def texture(self):
        return self.fbo_tx

    def bind_texture(self, tx_uni_loc, tx_id = 0):
        glActiveTexture(GL_TEXTURE0 + tx_id)
        glBindTexture(GL_TEXTURE_2D, self.fbo_tx)
        glUniform1i(tx_uni_loc, tx_id)


# Object wrapper for shapes in GLSL, builds GPU buffers holding vertex info`
# typically used by derived shapes (rectangle etc.)
class Shape:
    def __init__(self, name):
        self.name = name
        self.vertex_vbo = None
        self.texcoord_vbo = None
        self.normal_vbo = None
        self.att_vertex = -1
        self.att_normal = -1
        self.att_texcoord = -1
        self.nb_points = 0
        self.np_texcoord = None
        self.position = np.array([0.0, 0.0, 0.0])
        self.scaling = np.array([1.0, 1.0, 1.0])
        self.rotation = np.array([0.0, 0.0, 0.0])

    def setPosition(self, x, y, z):
        self.position[0] = x
        self.position[1] = y
        self.position[2] = z

    def getPosition(self):
        return self.position

    def getPositionMatrix(self):
        return translate(self.position[0], self.position[1], self.position[2])

    def setScaling(self, x, y, z):
        self.scaling[0] = x
        self.scaling[1] = y
        self.scaling[2] = z

    def getScaling(self):
        return self.scaling

    def getScalingMatrix(self):
        return scale(self.scaling[0], self.scaling[1], self.scaling[2])

    def setRotationX(self, angle):
        self.rotation[0] = angle
    
    def setRotationY(self, angle):
        self.rotation[1] = angle

    def setRotationZ(self, angle):
        self.rotation[2] = angle

    def getRotationMatrix(self):
        #TODO: use a cache system to reduce computations
        return rotate(self.rotation[0], 1.0, 0.0, 0.0).dot(
                rotate(self.rotation[1], 0.0, 1.0, 0.0)).dot(
                rotate(self.rotation[2], 0.0, 0.0, 1.0))

    def getMatrix(self):
        return self.getRotationMatrix().dot(self.getPositionMatrix()).dot(self.getScalingMatrix())

    def build_buffers(self, vertices, normals, tex_coords, lines=False):
        for val in vertices:
            if len(val) != 3:
                print('Invalid number of points in vertice ' + str(val))
                exit()
        self.nb_points = int(len(vertices))
        vertices = np.array(vertices, dtype=np.float32)
        if lines:
            self.type = GL_LINE_STRIP
        else:
            self.type = GL_TRIANGLES
        if normals!=None and len(normals) == 0:
            normals = None
        if tex_coords!=None and len(tex_coords) == 0:
            tex_coords = None

        # Generate buffers to hold our vertices
        self.vertex_vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_vbo)
        glBufferData(GL_ARRAY_BUFFER, self.nb_points*3*4, vertices, GL_STATIC_DRAW)
    
        if normals != None:
            if self.nb_points != len(normals):
                print('Invalid number of points in normals')
                exit()
            for val in normals:
                if len(val) != 3:
                    print('Invalid number of points in normals ' + str(val))
                    exit()
            normals = np.array(normals, dtype=np.float32)
            self.normal_vbo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.normal_vbo)
            glBufferData(GL_ARRAY_BUFFER, self.nb_points*3*4, normals, GL_STATIC_DRAW)

        if tex_coords != None:
            if self.nb_points != len(tex_coords):
                print('Invalid number of points in tex_coords ' + str(len(tex_coords)) + ' expecting ' + str(self.nb_points * 2))
                exit()
            for val in tex_coords:
                if len(val) != 2:
                    print('Invalid number of points in normals ' + str(val))
                    exit()
            tex_coords = np.array(tex_coords, dtype=np.float32)
            self.texcoord_vbo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.texcoord_vbo)
            glBufferData(GL_ARRAY_BUFFER, self.nb_points*2*4, tex_coords, GL_STATIC_DRAW)
            self.np_texcoord = tex_coords
            print('Tex coords ' + str(tex_coords))

        print('Buffers generated - Number of points ' + str(self.nb_points) + ' vertex_vbo ' + str(self.vertex_vbo) + ' normal_vbo ' + str(self.normal_vbo) + ' texcoord_vbo ' + str(self.texcoord_vbo))
        glBindBuffer(GL_ARRAY_BUFFER, 0)


    def draw(self, program):
        self.att_vertex = glGetAttribLocation(program, "aVertex")
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_vbo)
        glEnableVertexAttribArray(self.att_vertex)
        glVertexAttribPointer(self.att_vertex, 3, GL_FLOAT, False, 0, ctypes.c_void_p(0))

        if self.normal_vbo:
            self.att_normal = glGetAttribLocation(program, "aNormal")
            if self.att_normal>=0:
                glBindBuffer(GL_ARRAY_BUFFER, self.att_normal)
                glEnableVertexAttribArray(self.att_normal)
                glVertexAttribPointer(self.att_normal, 3, GL_FLOAT, False, 0, ctypes.c_void_p(0))

        if self.texcoord_vbo:
            self.att_texcoord = glGetAttribLocation(program, "aTexCoord")
            #print('att location ' + str(self.att_texcoord) )
            if self.att_texcoord>=0:
                glBindBuffer(GL_ARRAY_BUFFER, self.texcoord_vbo)
                glEnableVertexAttribArray(self.att_texcoord)
                glVertexAttribPointer(self.att_texcoord, 2, GL_FLOAT, False, 0, ctypes.c_void_p(0))

        #print('Buffers ready -  vertex_att ' + str(self.att_vertex) + ' normal_att ' + str(self.att_normal) + ' texcoord_att ' + str(self.att_texcoord))


        glDrawArrays(self.type, 0, self.nb_points)
        #disable vertex arrays
        glDisableVertexAttribArray(self.att_vertex)
        if self.att_normal>=0:
            glDisableVertexAttribArray(self.att_normal)
        if self.att_texcoord>=0:
            glDisableVertexAttribArray(self.att_texcoord)
        glBindBuffer(GL_ARRAY_BUFFER, 0)


# Class object
class OBJ :
    generate_on_init = True
    @classmethod
    def loadMaterial(cls, filename):
        contents = {}
        mtl = None
        dirname = os.path.dirname(filename)

        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'newmtl':
                mtl = contents[values[1]] = {}
            elif mtl is None:
                raise ValueError("mtl file doesn't start with newmtl stmt")
            elif values[0] == 'map_Kd':
                # load the texture referred to by this declaration
                mtl[values[0]] = values[1]
                imagefile = os.path.join(dirname, mtl['map_Kd'])
                mtl['texture_Kd'] = Texture(imagefile)
            else:
                mtl[values[0]] = list(map(float, values[1:]))
        return contents

    def __init__(self, filename, swapyz=False):
        """Loads a Wavefront OBJ file. """
        loc_vertices = []
        loc_normals = []
        loc_texcoords = []
        loc_faces = []
        loc_mtl = None
        material = None
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                loc_vertices.append(v)
            elif values[0] == 'vn':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                loc_normals.append(v)
            elif values[0] == 'vt':
                loc_texcoords.append(list(map(float, values[1:3])))
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                #loc_mtl.append(self.loadMaterial(os.path.join(filename, values[1])))
                loc_mtl = self.loadMaterial(os.path.join(values[1]))
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                loc_faces.append((face, norms, texcoords, material))

        all_vertices = []
        all_normals = []
        all_texcoords = []
        self.shapes = []
        prev_mat = None
        for face in loc_faces:
            vertices, normals, texture_coords, material = face
            if material != prev_mat:
                if len(all_vertices) > 0:
                    myShape = Shape("shapy")
                    myShape.build_buffers(all_vertices, all_normals, all_texcoords)
                    myShape.mtl = loc_mtl[prev_mat]
                    self.shapes.append(myShape)
                all_vertices = []
                all_normals = []
                all_texcoords = []
                prev_mat = material
            
            for i in range(len(vertices)):
                if i == 3:
                    if normals[i] > 0:
                        all_normals.append(loc_normals[normals[i-3] - 1])
                        all_normals.append(loc_normals[normals[i-1] - 1])
                    if texture_coords[i] > 0:
                        all_texcoords.append(loc_texcoords[texture_coords[i-3] - 1])
                        all_texcoords.append(loc_texcoords[texture_coords[i-1] - 1])
                    all_vertices.append(loc_vertices[vertices[i-3] - 1])
                    all_vertices.append(loc_vertices[vertices[i-1] - 1])

                if normals[i] > 0:
                    all_normals.append(loc_normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    all_texcoords.append(loc_texcoords[texture_coords[i] - 1])
                all_vertices.append(loc_vertices[vertices[i] - 1])

        if len(all_vertices):
            myShape = Shape("shapy")
            myShape.build_buffers(all_vertices, all_normals, all_texcoords)
            myShape.mtl = loc_mtl[prev_mat]
            prev_mat = material
            self.shapes.append(myShape)

    # Drawing the object 
    def draw(self, program, sTexture):
        for shape in self.shapes:
            if 'texture_Kd' in shape.mtl:
                shape.mtl['texture_Kd'].activate(sTexture)
            shape.draw(program)




# Rectangle shape, with texture units and no normal
# use flip=True in init to flip texture vertically
class Rectangle(Shape):
    def __init__(self, name, flip = False):
        Shape.__init__(self, name)
        ty_min = 0.0
        ty_max = 1.0
        if flip == True:
            ty_min = 1.0
            ty_max = 0.0

        self.build_buffers(
            [( -1.000000, -1.000000, 0.000000),
            ( 1.000000, -1.000000, 0.000000),
            ( 1.000000, 1.000000, 0.000000),
            ( -1.000000, -1.000000, 0.000000),
            ( 1.000000, 1.000000, 0.000000),
            ( -1.000000, 1.000000, 0.000000)],
            None,
            [(0.0, ty_min),
            (1.0, ty_min),
            (1.0, ty_max),
            (0.0, ty_min),
            (1.0, ty_max),
            (0.0, ty_max)]
        )

class Cube(Shape): 
    def __init__(self, name, flip = False):
        Shape.__init__(self, name)
        ty_min = 0.0
        ty_max = 1.0
        if flip == True:
            ty_min = 1.0
            ty_max = 0.0

        self.build_buffers(
            [
            ### back face
            ( -1.0, -1.0, -1.0),
            ( 1.0, -1.0, -1.0),
            ( 1.0, 1.0, -1.0),
            ( -1.0, -1.0, -1.0),
            ( 1.0, 1.0, -1.0),
            ( -1.0, 1.0, -1.0),

            ### front face
            ( -1.0, -1.0, 1.0),
            ( 1.0, -1.0, 1.0),
            ( 1.0, 1.0, 1.0),
            ( -1.0, -1.0, 1.0),
            ( 1.0, 1.0, 1.0),
            ( -1.0, 1.0, 1.0),

            ### top face
            (-1.0, 1.0, 1.0),
            (1.0, 1.0, 1.0),
            (1.0, 1.0, -1.0),
            (-1.0, 1.0, 1.0),
            (1.0, 1.0, -1.0),
            (-1.0, 1.0, -1.0),

            ### bottom face
            (-1.0, -1.0, 1.0),
            (1.0, -1.0, 1.0),
            (1.0, -1.0, -1.0),
            (-1.0, -1.0, 1.0),
            (1.0, -1.0, -1.0),
            (-1.0, -1.0, -1.0),

            ### right face
            (1.0, -1.0, -1.0),
            (1.0, -1.0, 1.0),
            (1.0, 1.0, 1.0),
            (1.0, -1.0, -1.0),
            (1.0, 1.0, 1.0),
            (1.0, 1.0, -1.0),

            ### left face
            (-1.0, -1.0, -1.0),
            (-1.0, -1.0, 1.0),
            (-1.0, 1.0, 1.0),
            (-1.0, -1.0, -1.0),
            (-1.0, 1.0, 1.0),
            (-1.0, 1.0, -1.0),
            ],
            None,
            [
            ### back face
            (0.0, ty_min),
            (1.0, ty_min),
            (1.0, ty_max),
            (0.0, ty_min),
            (1.0, ty_max),
            (0.0, ty_max),
            
            ### front face
            (0.0, ty_min),
            (1.0, ty_min),
            (1.0, ty_max),
            (0.0, ty_min),
            (1.0, ty_max),
            (0.0, ty_max),

            ### top face
            (0.0, ty_min),
            (1.0, ty_min),
            (1.0, ty_max),
            (0.0, ty_min),
            (1.0, ty_max),
            (0.0, ty_max),

            ### bottom face
            (0.0, ty_min),
            (1.0, ty_min),
            (1.0, ty_max),
            (0.0, ty_min),
            (1.0, ty_max),
            (0.0, ty_max),

            ### right face
            (0.0, ty_min),
            (1.0, ty_min),
            (1.0, ty_max),
            (0.0, ty_min),
            (1.0, ty_max),
            (0.0, ty_max),

            ### left face
            (0.0, ty_min),
            (1.0, ty_min),
            (1.0, ty_max),
            (0.0, ty_min),
            (1.0, ty_max),
            (0.0, ty_max),
            ]
        )



#creates a rotation matrix of angle (in degrees) around axis vec3(x,y,z)
def rotate(angle, x, y, z):
    s = math.sin(math.radians(angle))
    c = math.cos(math.radians(angle))
    magnitude = math.sqrt(x*x + y*y + z*z)
    nc = 1 - c
      
    x /= magnitude
    y /= magnitude
    z /= magnitude

    return np.array([
        [     c + x**2 * nc, y * x * nc - z * s, z * x * nc + y * s, 0],
        [y * x * nc + z * s,      c + y**2 * nc, y * z * nc - x * s, 0],
        [z * x * nc - y * s, z * y * nc + x * s,      c + z**2 * nc, 0],
        [                 0,                  0,                  0, 1],
    ])

#creates a translation matrix of vec3(x,y,z)
def translate(x, y, z):
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [x, y, z, 1],
    ])

#creates a scale matrix
def scale(x, y, z):
    return np.array([
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1],
    ])


#creates a perspective projection matrix
# - fovy: field of view along vertical axis
# - aspect: aspect ratio (width/height)
# - z_near: z coord of near z clipping plane
# - z_far: z coord of far z clipping plane
def perspective(fovy, aspect, z_near, z_far):
    f = 1 / math.tan(math.radians(fovy) / 2)
    return np.array([
        [f / aspect,  0,                                   0,  0],
        [          0, f,                                   0,  0],
        [          0, 0, (z_far + z_near) / (z_near - z_far), -1],
        [          0, 0, (2*z_far*z_near) / (z_near - z_far),  0]
    ])


#creates an orthogonal perspective projection matrix
def ortho(left, right, top, bottom, z_near, z_far):
    m11 = 2 / (right-left)
    m22 = 2 / (top-bottom)
    m33 = -2 / (z_far-z_near)
    m34 = (right+left) / (right-left)
    m42 = (top+bottom) / (top-bottom)
    m43 = (z_far+z_near) / (z_far-z_near)
    return np.array([
        [m11, 0, 0,  0],
        [0, m22, 0,  0],
        [0, 0, m33, m34],
        [0, m42, m43, 1]
    ])

#creates a lookat view matrix looking at center from eye with up-vector equal to Y axis
def lookat(eye, center):
    zaxis = center - eye
    zaxis = zaxis.normalize()
    up = pygame.math.Vector3(0, 1, 0)

    xaxis = zaxis.cross(up).normalize()
    yaxis = xaxis.cross(zaxis).normalize()
    zaxis = -zaxis

    return np.array([
        [xaxis.x, xaxis.y, xaxis.z, -xaxis.dot(eye)],
        [yaxis.x, yaxis.y, yaxis.z, -yaxis.dot(eye)],
        [zaxis.x, zaxis.y, zaxis.z, -zaxis.dot(eye)],
        [0, 0, 0, 1]
    ]).transpose().dot(scale(1, -1, 1))



