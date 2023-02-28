from feather.shapes.shape import Shape

class Land(Shape):
    def __init__(self, name, flip, droite, gauche, plafond, scene = None):
        Shape.__init__(self, name, scene)
        self.droite = droite
        self.gauche = gauche
        self.plafond = plafond
        plafond
        ty_min = 0.0
        ty_max = 1.0
        if flip == True:
            ty_min = 1.0
            ty_max = 0.0

        self.setScaling(1, 1, 1)

        array0 = []
        array1 =[]
        if plafond == True :
            array0 += [(-1.0, 1.0, 1.0),
                        (1.0, 1.0, 1.0),
                        (1.0, 1.0, -1.0),
                        (-1.0, 1.0, 1.0),
                        (1.0, 1.0, -1.0),
                        (-1.0, 1.0, -1.0)]

            array1 += [(0.0, ty_min),
                        (1.0, ty_min),
                        (1.0, ty_max),
                        (0.0, ty_min),
                        (1.0, ty_max),
                        (0.0, ty_max)]

        array0 += [(-1.0, -1.0, 1.0),
                    (1.0, -1.0, 1.0),
                    (1.0, -1.0, -1.0),
                    (-1.0, -1.0, 1.0),
                    (1.0, -1.0, -1.0),
                    (-1.0, -1.0, -1.0)]

        array1 += [(0.0, ty_min),
                    (1.0, ty_min),
                    (1.0, ty_max),
                    (0.0, ty_min),
                    (1.0, ty_max),
                    (0.0, ty_max)]

        if droite :
            array0 += [(1.0, -1.0, -1.0),
                        (1.0, -1.0, 1.0),
                        (1.0, 1.0, 1.0),
                        (1.0, -1.0, -1.0),
                        (1.0, 1.0, 1.0),
                        (1.0, 1.0, -1.0)]

            array1 += [(0.0, ty_min),
                        (1.0, ty_min),
                        (1.0, ty_max),
                        (0.0, ty_min),
                        (1.0, ty_max),
                        (0.0, ty_max)]

        if gauche :
            array0 += [(-1.0, -1.0, -1.0),
                        (-1.0, -1.0, 1.0),
                        (-1.0, 1.0, 1.0),
                        (-1.0, -1.0, -1.0),
                        (-1.0, 1.0, 1.0),
                        (-1.0, 1.0, -1.0)]
            
            array1 += [(0.0, ty_min),
                        (1.0, ty_min),
                        (1.0, ty_max),
                        (0.0, ty_min),
                        (1.0, ty_max),
                        (0.0, ty_max)]

        self.build_buffers(
            array0,
            None,
            array1
        )


    def setScaling(self, x, y, z):
        return super().setScaling(x*0.5, y*0.5, z*0.5)