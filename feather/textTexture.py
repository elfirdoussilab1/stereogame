from PIL import Image
import numpy as np
from OpenGL.GL import *
import pygame

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
class TextTexture:
    def __init__(self, text: str, color, bgColor):
        img = pygame.font.Font(None, 200).render(text, True, color, bgColor)
        w, h = img.get_size()
        self.texture = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        data = pygame.image.tostring(img, "RGBA", 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)

    def activate(self, tx_uni_loc, tx_id=0):
        glActiveTexture(GL_TEXTURE0 + tx_id)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glUniform1i(tx_uni_loc, tx_id)
