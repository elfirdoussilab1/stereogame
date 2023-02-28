import os
from feather import Program

filePath = os.path.dirname(os.path.abspath(__file__))
class Interlacer(Program):
    def __init__(self):
        ### load shader code
        with open(os.path.join(filePath, 'shaders/interlaceVertex.glsl'), 'r') as file:
            interlacerVertex = file.read()
        with open(os.path.join(filePath, 'shaders/interlaceFloatFragment.glsl'), 'r') as file:
            interlacerFragment = file.read()

        ### init program
        super().__init__(interlacerVertex, interlacerFragment)

        self.sTextures = [self.getUniformLocation(f"sTextures[{i}]") for i in range(8)] 

    def setTextureFromFBO(self, fbo, index):
        fbo.bind_texture(self.sTextures[index], index)

    def setTextureFromImage(self, texture, index):
        texture.activate(self.sTextures[index], index)