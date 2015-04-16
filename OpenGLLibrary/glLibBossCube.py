#!/usr/bin/env python
import pygame
from pygame.locals import *

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print ('Floatmotion requires PyOpenGL')
    raise SystemExit



#some simple data for a colored cube
#here we have the 3D point position and color
#for each corner. then we have a list of indices
#that describe each face, and a list of indieces
#that describes each edge


CUBE_POINTS = (
    (0.5, -0.5, -0.5),  (0.5, 0.5, -0.5),
    (-0.5, 0.5, -0.5),  (-0.5, -0.5, -0.5),
    (0.5, -0.5, 0.5),   (0.5, 0.5, 0.5),
    (-0.5, -0.5, 0.5),  (-0.5, 0.5, 0.5)
)

#colors are 0-1 floating values
CUBE_COLORS = (
    (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0),
    (1, 0, 1), (1, 1, 1), (0, 0, 1), (0, 1, 1)
)

CUBE_QUAD_VERTS = (
    (0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4),
    (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6)
)

CUBE_EDGES = (
    (0,1), (0,3), (0,4), (2,1), (2,3), (2,7),
    (6,3), (6,4), (6,7), (5,1), (5,4), (5,7),
)

allpoints = zip(CUBE_POINTS, CUBE_COLORS)

class glLibObj():
    def draw(self,pos=[0,0,0],rotations=[],scalar=1.0):
        glPushMatrix()
        glTranslatef(*pos)
        for rotation in rotations:
            if rotation[0] != 0: glRotatef(rotation[0],1,0,0)
            if rotation[1] != 0: glRotatef(rotation[1],0,1,0)
            if rotation[2] != 0: glRotatef(rotation[2],0,0,1)
        glScalef(scalar,scalar,scalar)
        glCallList(self.list)
        glPopMatrix()
    def __del__(self):
        del self.list

class glLibObjBossCube(glLibObj):
    def __init__(self,size=1.5,x=0,y=0,z=0,speed_x=0,speed_y=0,speed_z=0,a=255,rotate_x=0,rotate_y=0,rotate_z=0,cube_type=0,time=-1):
        self.size=size

        self.x=x
        self.y=y
        self.z=z
        self.speed_x=speed_x
        self.speed_y=speed_y
        self.speed_z=speed_z

        self.a=a

        self.rotate_x=rotate_x
        self.rotate_y=rotate_y
        self.rotate_z=rotate_z

        self.cube_type=cube_type
        self.time=time

        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)
        glBegin(GL_QUADS)
        for face in CUBE_QUAD_VERTS:
            for vert in face:
                pos, color = allpoints[vert]
                glColor3fv(color)
                glVertex3fv(pos)
        glEnd()

        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_LINES)
        for line in CUBE_EDGES:
            for vert in line:
                pos, color = allpoints[vert]
                glVertex3fv(pos)

        glEnd()
        glEndList()
        
