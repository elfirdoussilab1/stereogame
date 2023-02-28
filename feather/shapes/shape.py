import numpy as np
from OpenGL.GL import *
from feather.transform import Transform
from feather.algebra import *
from feather.materials import DefaultMaterial

# Object wrapper for shapes in GLSL, builds GPU buffers holding vertex info`
# typically used by derived shapes (rectangle etc.)
class Shape(Transform):
    def __init__(self, name, scene = None):
        Transform.__init__(self)
        self.name = name
        self.vertex_vbo = None
        self.texcoord_vbo = None
        self.normal_vbo = None
        self.att_vertex = -1
        self.att_normal = -1
        self.att_texcoord = -1
        self.nb_points = 0
        self.np_texcoord = None
        self.scene = scene
        self.vertices = None
        self.normals = None
        self.texcoords = None

        self.material = DefaultMaterial()

        self.scene = scene

        ###FIXME: shoud not be here
        self.hasInvertedPerspective = False

        if self.scene is not None:
            self.scene.addShape(self)


    def setMaterial(self, material):
        self.material = material

    def render(self, perspective_mx, model_matrix, view_matrix):
        mv_matrix = self.getMatrix().dot(model_matrix).dot(view_matrix)
        if(self.material is None):
            print(f"ERROR : {name} shape has no material (consider using setMaterial)")
        self.material.use(perspective_mx, mv_matrix)
        self.material.update()
        self.draw(self.material.program)

    def build_buffers(self, vertices, normals, tex_coords, lines=False):
        for val in vertices:
            if len(val) != 3:
                print('Invalid number of points in vertice ' + str(val))
                exit()
        self.nb_points = int(len(vertices))

        self.vertices = vertices
        self.normals = normals
        self.texcoords = tex_coords

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
                #print('Invalid number of points in tex_coords ' + str(len(tex_coords)) + ' expecting ' + str(self.nb_points * 2))
                exit()
            for val in tex_coords:
                if len(val) != 2:
                    #print('Invalid number of points in normals ' + str(val))
                    exit()
            tex_coords = np.array(tex_coords, dtype=np.float32)
            self.texcoord_vbo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.texcoord_vbo)
            glBufferData(GL_ARRAY_BUFFER, self.nb_points*2*4, tex_coords, GL_STATIC_DRAW)
            self.np_texcoord = tex_coords
            #print('Tex coords ' + str(tex_coords))

        #print('Buffers generated - Number of points ' + str(self.nb_points) + ' vertex_vbo ' + str(self.vertex_vbo) + ' normal_vbo ' + str(self.normal_vbo) + ' texcoord_vbo ' + str(self.texcoord_vbo))
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

    def setScene(self,scene):
        self.scene = scene
        
    def destroy(self):
        self.scene.removeShape(self)
