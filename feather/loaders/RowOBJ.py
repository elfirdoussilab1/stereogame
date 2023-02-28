import os
import pygame
from OpenGL.GL import *
from feather.shapes.shape import Shape

class RowOBJ(Shape):
    generate_on_init = True
    @classmethod
    def loadTexture(cls, imagefile):
        surf = pygame.image.load(imagefile)
        image = pygame.image.tostring(surf, 'RGBA', 1)
        ix, iy = surf.get_rect().size
        texid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texid)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        return texid

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
                mtl['texture_Kd'] = cls.loadTexture(imagefile)
            else:
                mtl[values[0]] = list(map(float, values[1:]))
        return contents

    def __init__(self, filename, swapyz=False, scene=None):
        """Loads a Wavefront OBJ file. """
        Shape.__init__(self, filename, scene)
        loc_vertices = []
        loc_normals = []
        loc_texcoords = []
        loc_faces = []
        
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
            #elif values[0] in ('usemtl', 'usemat'):
            #    material = values[1]
            #elif values[0] == 'mtllib':
            #    self.mtl = self.loadMaterial(os.path.join(filename, values[1]))
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
        for face in loc_faces:
            vertices, normals, texture_coords, material = face
            
            
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

        print('Model loaded')
        self.build_buffers(all_vertices, all_normals, all_texcoords)
        print('Buffer created')
