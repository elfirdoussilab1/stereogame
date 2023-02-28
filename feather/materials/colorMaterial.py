import os
from feather import Program

filePath = os.path.dirname(os.path.abspath(__file__))

class ColorMaterial(Program):
    def __init__(self, r, g, b):
        with open(os.path.join(filePath, 'shaders/fboVertex.glsl'), 'r') as file:
            vs_tx = file.read()

        with open(os.path.join(filePath, 'shaders/flatFragment.glsl'), 'r') as file:
            fs_flat = file.read()

        super().__init__(vs_tx, fs_flat)
        self.color = (r, g, b)

    def update(self):
        self.setVector4("color", self.color[0], self.color[1], self.color[2], 1.0)