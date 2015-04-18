'''OpenGL extension OES.texture_3D

This module customises the behaviour of the 
OpenGL.raw.GLES2.OES.texture_3D to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/OES/texture_3D.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.OES.texture_3D import *
from OpenGL.raw.GLES2.OES.texture_3D import _EXTENSION_NAME

def glInitTexture3DOES():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

# INPUT glTexImage3DOES.pixels size not checked against 'format,type,width,height,depth'
glTexImage3DOES=wrapper.wrapper(glTexImage3DOES).setInputArraySize(
    'pixels', None
)
# INPUT glTexSubImage3DOES.pixels size not checked against 'format,type,width,height,depth'
glTexSubImage3DOES=wrapper.wrapper(glTexSubImage3DOES).setInputArraySize(
    'pixels', None
)
# INPUT glCompressedTexImage3DOES.data size not checked against imageSize
glCompressedTexImage3DOES=wrapper.wrapper(glCompressedTexImage3DOES).setInputArraySize(
    'data', None
)
# INPUT glCompressedTexSubImage3DOES.data size not checked against imageSize
glCompressedTexSubImage3DOES=wrapper.wrapper(glCompressedTexSubImage3DOES).setInputArraySize(
    'data', None
)
### END AUTOGENERATED SECTION