from feather.shapes.shape import Shape

class Cube(Shape):
    def __init__(self, name, flip, scene = None):
        Shape.__init__(self, name, scene)
        ty_min = 0.0
        ty_max = 1.0
        if flip == True:
            ty_min = 1.0
            ty_max = 0.0

        self.setScaling(1, 1, 1)

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


    def setScaling(self, x, y, z):
        return super().setScaling(x*0.5, y*0.5, z*0.5)