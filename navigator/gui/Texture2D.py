#[MIT license:]
#
# Copyright (c) 2004  Dave Pape
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from OpenGL.GL import *
from OpenGL.GLU import *
import Image


class Texture2D:
    def __init__(self, file, wrap=GL_REPEAT, minFilter=GL_LINEAR, magFilter=GL_LINEAR, texenv=GL_MODULATE):
        self.file = file
        self.wrapS = wrap
        self.wrapT = wrap
        self.minFilter = minFilter
        self.magFilter = magFilter
        self.texenv = texenv
        self.defined = False
        self.id = 0

    def define(self):
        img = Image.open(self.file).transpose(Image.FLIP_TOP_BOTTOM).convert('RGBA')
        width = 2
        while width < img.size[0]: width *= 2
        width /= 2
        height = 2
        while height < img.size[1]: height *= 2
        height /= 2
        if (width != img.size[0]) or (height != img.size[1]):
            img = img.resize((width,height))
        
        self.id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, self.wrapS)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, self.wrapT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, self.minFilter)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, self.magFilter)
        if (self.minFilter == GL_NEAREST_MIPMAP_NEAREST) or \
           (self.minFilter == GL_NEAREST_MIPMAP_LINEAR) or \
           (self.minFilter == GL_LINEAR_MIPMAP_NEAREST) or \
           (self.minFilter == GL_LINEAR_MIPMAP_LINEAR):
              gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGBA, img.size[0], img.size[1],
                                GL_RGBA, GL_UNSIGNED_BYTE, img.tostring())
        else:
              glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1],
                           0, GL_RGBA, GL_UNSIGNED_BYTE, img.tostring())
        glBindTexture(GL_TEXTURE_2D, 0)
        self.defined = True

    def apply(self):
        if not self.defined:
            self.define()
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, self.texenv)
        glBindTexture(GL_TEXTURE_2D, self.id)
        if self.id != 0:
            glEnable(GL_TEXTURE_2D)
        else:
            glDisable(GL_TEXTURE_2D)

    def disable(self):
        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)

