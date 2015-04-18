'''OpenGL extension ARB.compute_shader

This module customises the behaviour of the 
OpenGL.raw.GL.ARB.compute_shader to provide a more 
Python-friendly API

Overview (from the spec)
	
	Recent graphics hardware has become extremely powerful and a strong desire
	to harness this power for work (both graphics and non-graphics) that does
	not fit the traditional graphics pipeline well has emerged. To address
	this, this extension adds a new single-stage program type known as a
	compute program. This program may contain one or more compute shaders
	which may be launched in a manner that is essentially stateless. This allows
	arbitrary workloads to be sent to the graphics hardware with minimal
	disturbance to the GL state machine.
	
	In most respects, a compute program is identical to a traditional OpenGL
	program object, with similar status, uniforms, and other such properties.
	It has access to many of the same resources as fragment and other shader
	types, such as textures, image variables, atomic counters, and so on.
	However, it has no predefined inputs nor any fixed-function outputs. It
	cannot be part of a pipeline and its visible side effects are through its
	actions on images and atomic counters.
	
	OpenCL is another solution for using graphics processors as generalized
	compute devices. This extension addresses a different need. For example,
	OpenCL is designed to be usable on a wide range of devices ranging from
	CPUs, GPUs, and DSPs through to FPGAs. While one could implement GL on these
	types of devices, the target here is clearly GPUs. Another difference is
	that OpenCL is more full featured and includes features such as multiple
	devices, asynchronous queues and strict IEEE semantics for floating point
	operations. This extension follows the semantics of OpenGL - implicitly
	synchronous, in-order operation with single-device, single queue
	logical architecture and somewhat more relaxed numerical precision
	requirements. Although not as feature rich, this extension offers several
	advantages for applications that can tolerate the omission of these
	features. Compute shaders are written in GLSL, for example and so code may
	be shared between compute and other shader types. Objects are created and
	owned by the same context as the rest of the GL, and therefore no
	interoperability API is required and objects may be freely used by both
	compute and graphics simultaneously without acquire-release semantics or
	object type translation.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/ARB/compute_shader.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.ARB.compute_shader import *
from OpenGL.raw.GL.ARB.compute_shader import _EXTENSION_NAME

def glInitComputeShaderARB():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION