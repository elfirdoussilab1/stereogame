# Class object
import os
from feather.materials.textureMaterial import TextureMaterial
from feather.texture import Texture
from feather.shapes.shape import Shape


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

    def __init__(self, filename, swapyz, scene):
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
            myShape = Shape("shapy", scene)
            myShape.build_buffers(all_vertices, all_normals, all_texcoords)
            myShape.mtl = loc_mtl[prev_mat]
            print(myShape.mtl)
            myShapeMat = TextureMaterial(myShape.mtl['texture_Kd'])
            myShape.setMaterial(myShapeMat)
            prev_mat = material
            self.shapes.append(myShape)

    # Drawing the object 
    def draw(self, program, sTexture):
        for shape in self.shapes:
            if 'texture_Kd' in shape.mtl:
                shape.mtl['texture_Kd'].activate(sTexture)
            shape.draw(program)