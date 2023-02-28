from OpenGL.GL import *

class Scene():
    def __init__(self):
        self.shapes = []

    def addShape(self, shape):
        self.shapes.append(shape)

    def removeShape(self, shape):
        shapes = []
        for shapy in self.shapes:
            if shapy != shape:
                shapes.append(shapy)
        self.shapes = shapes
        del shape

    def render(self, perspective_mx, model_matrix, view_matrix):
        glClearColor(0.0, 0.0, 0.2, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)

        ### Rendu des objets de la scène ###

        for shape in self.shapes:
            shape.render(perspective_mx, model_matrix, view_matrix)


    def renderAlioscopy(self, perspective_mx1, perspective_mx2, view_matrix1, view_matrix2, model_matrix):
        glClearColor(0.0, 0.0, 0.2, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)

        ### Rendu des objets de la scène ###

        for shape in self.shapes:
            if shape.hasInvertedPerspective:
                shape.render(perspective_mx2, model_matrix, view_matrix2)
            else:
                shape.render(perspective_mx1, model_matrix, view_matrix1)