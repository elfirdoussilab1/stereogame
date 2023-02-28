from OpenGL.GL import *

# Object wrapping openGL offscreen framebuffer setup
# to build FBO:
# fbo = FrameBuffer(offs_w, offs_h)
#
# to set FBO the current render target:
# fbo.bind()
#
# to bind fbo underlying texture to uniform (same as with texture.activate):
# fbo.bind_texture(uniform_tx)
#
# If multiple textures in fragment shader, start from max texture unit to first one, eg:
# fbo.bind_texture(uniform_tx2, 1)
# fbo.bind_texture(uniform_tx1, 0)
#
class FrameBuffer:
    def __init__(self, width, height):
        self.fbo = GLuint()
        glGenFramebuffers(1, self.fbo)
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        self.fbo_tx = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.fbo_tx)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.fbo_tx, 0)

        rbo = GLuint()
        glGenRenderbuffers(1, rbo)
        glBindRenderbuffer(GL_RENDERBUFFER, rbo)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, width, height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, rbo)

        if not glCheckFramebufferStatus(GL_FRAMEBUFFER) == GL_FRAMEBUFFER_COMPLETE:
            print('framebuffer binding failed')
            exit()
        self.width = width
        self.height = height

    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)

    def texture(self):
        return self.fbo_tx

    def bind_texture(self, tx_uni_loc, tx_id = 0):
        glActiveTexture(GL_TEXTURE0 + tx_id)
        glBindTexture(GL_TEXTURE_2D, self.fbo_tx)
        glUniform1i(tx_uni_loc, tx_id)