import os
from feather import Program

filePath = os.path.dirname(os.path.abspath(__file__))

class TextureMaterial(Program):
    def __init__(self, texture):
        with open(os.path.join(filePath, 'shaders/fboVertex.glsl'), 'r') as file:
            vs_tx = file.read()

        with open(os.path.join(filePath, 'shaders/fboFragment.glsl'), 'r') as file:
            fs_tx = file.read()

        super().__init__(vs_tx, fs_tx)
        self.texture = texture

    def update(self):
        self.setTexture("sTexture", self.texture)