from PIL import Image
import numpy as np
from OpenGL.GL import *

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
