import threading
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import glutSolidTeapot
import glLibOBJLoad
import glLibOBJLoad_threading
from glLibLocals import *
from glLibTexturing import *
from math import *
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
class glLibObjText(glLibObj):
    def __init__(self,text,font,color,filters=[],bgcolor=None):
        if bgcolor:s1 = font.render(text,False,color,bgcolor)
        else:s1 = font.render(text,False,color)
        s1size = s1.get_size()
        exp1 = log(s1size[0],2)
        xsize = 2**(int(exp1)+1)
        exp2 = log(s1size[1],2)
        ysize = 2**(int(exp2)+1)
        s2 = pygame.Surface((xsize,ysize))
        index = 0
        colors = [(0,0,0),(100,100,100),(200,200,200)]
        for c in colors:
            if c == color: index += 1; continue
            elif c == bgcolor: index += 1; continue
            else: break
        s2.fill(colors[index])
        s2.blit(s1,(0,ysize-s1size[1]))
        s2.set_colorkey(colors[index])
        texture = glLibTexture(s2,filters)
        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)
        glLibSelectTexture(texture)
        x = s1size[0]/float(xsize)
        y = s1size[1]/float(ysize)
        h = 1.0
        w = float(s1size[0])/s1size[1] #w/1.0 = s1size[0]/s1size[1]
        glBegin(GL_QUADS)
        glNormal3f(0,0,1)
        glTexCoord2f(0,0);glVertex3f(0,0,0)
        glTexCoord2f(x,0);glVertex3f(w,0,0)
        glTexCoord2f(x,y);glVertex3f(w,h,0)
        glTexCoord2f(0,y);glVertex3f(0,h,0)
        glEnd()
        glEndList()
class glLibObjUser(glLibObj):
    def __init__(self,path):
        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)
    def finish(self):
        glEndList()
class glLibObjFromFile(glLibObj):
    def __init__(self,path,x=0,y=0,z=0,speed_x=0,speed_y=0,speed_z=0):
        self.x=x
        self.y=y
        self.z=z
        self.speed_x=speed_x
        self.speed_y=speed_y
        self.speed_z=speed_z
        self.list = glLibOBJLoad.OBJ(path).gl_list
class glLibObjFromFile_threading(glLibObj):
    def __init__(self,path,x=0,y=0,z=0,speed_x=0,speed_y=0,speed_z=0):
        self.x=x
        self.y=y
        self.z=z
        self.speed_x=speed_x
        self.speed_y=speed_y
        self.speed_z=speed_z

        t = threading.Thread(target=glLibObjFromFile_threading.do_work, args=(self,path,glLibObj))
        t.daemon = True
        t.start()
        self.list = glLibOBJLoad.OBJ(path).gl_list
        #glLibObjFromFile_threading.do_work(self,path,glLibObj)

    def do_work(self, path,glLibObj):
        print "Hallo"
        self.list = glLibOBJLoad.OBJ(path).gl_list
        print "Fertig"
class glLibObjCube(glLibObj):
    def __init__(self,size=0.5,x=0,y=0,z=0,speed_x=0,speed_y=0,speed_z=0,r=255,g=255,b=255,a=255,cube_type=0,time=-1):
        self.size=size

        self.x=x
        self.y=y
        self.z=z
        self.speed_x=speed_x
        self.speed_y=speed_y
        self.speed_z=speed_z

        self.r=r
        self.g=g
        self.b=b
        self.a=a

        self.cube_type=cube_type
        self.time=time

        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)
        glBegin(GL_QUADS)
        glNormal3f( 0.0, 0.0, 1.0);glVertex3f(-size,-size, size);glVertex3f( size,-size, size);glVertex3f( size, size, size);glVertex3f(-size, size, size)
        glNormal3f( 0.0, 0.0,-1.0);glVertex3f(-size,-size,-size);glVertex3f(-size, size,-size);glVertex3f( size, size,-size);glVertex3f( size,-size,-size)
        glNormal3f( 0.0, 1.0, 0.0);glVertex3f(-size, size,-size);glVertex3f(-size, size, size);glVertex3f( size, size, size);glVertex3f( size, size,-size)
        glNormal3f( 0.0,-1.0, 0.0);glVertex3f(-size,-size,-size);glVertex3f( size,-size,-size);glVertex3f( size,-size, size);glVertex3f(-size,-size, size)
        glNormal3f( 1.0, 0.0, 0.0);glVertex3f( size,-size,-size);glVertex3f( size, size,-size);glVertex3f( size, size, size);glVertex3f( size,-size, size)
        glNormal3f(-1.0, 0.0, 0.0);glVertex3f(-size,-size,-size);glVertex3f(-size,-size, size);glVertex3f(-size, size, size);glVertex3f(-size, size,-size)
        glEnd()
        glEndList()
class glLibObjStar:
    def __init__(self,size=0.5,x=0,y=0,z=0,speed_x=0,speed_y=0,speed_z=0,r=255,g=255,b=255,a=255,star_type=0,time=-1):
        self.size=size

        self.x=x
        self.y=y
        self.z=z
        self.speed_x=speed_x
        self.speed_y=speed_y
        self.speed_z=speed_z

        self.r=r
        self.g=g
        self.b=b
        self.a=a

        self.star_type=star_type
        self.time=time
class glLibObjTeapot(glLibObj):
    def __init__(self,size=1.0):
        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)
        try:glutSolidTeapot(size)
        except:print "Teapot loading failed!  Upgrade your OpenGL!"
        glEndList()
class glLibObjSphere(glLibObj):
    def __init__(self,detail):
        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)
        Sphere = gluNewQuadric()
        gluSphere(Sphere,1.0,detail,detail)
        glEndList()
class glLibObjTexSphere(glLibObj):
    def __init__(self,radius,detail,x=0,y=0,z=0,speed_x=0,speed_y=0,speed_z=0,r=255,g=255,b=255,a=255,rotate_x=0,rotate_y=0,rotate_z=0,sphere_type=0,time=-1):
        self.radius=radius
        self.detail=detail

        self.x=x
        self.y=y
        self.z=z
        self.speed_x=speed_x
        self.speed_y=speed_y
        self.speed_z=speed_z

        self.r=r
        self.g=g
        self.b=b
        self.a=a

        self.rotate_x=rotate_x
        self.rotate_y=rotate_y
        self.rotate_z=rotate_z

        self.sphere_type=sphere_type
        self.time=time

        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)
        Sphere = gluNewQuadric()
        gluQuadricTexture(Sphere,GLU_TRUE)
        gluSphere(Sphere,radius,detail,detail)
        glEndList()
class glLibObjCylinder(glLibObj):
    def __init__(self,radius,length,detail):
        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)
        Cylinder = gluNewQuadric()
        gluCylinder(Cylinder,radius,radius,length,detail,1)
        glEndList()
class glLibObjTexCylinder(glLibObj):
    def __init__(self,radius,length,detail):
        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)
        Cylinder = gluNewQuadric()
        gluQuadricTexture(Cylinder,GLU_TRUE)
        gluCylinder(Cylinder,radius,radius,length,detail,1)
        glEndList()
class glLibObjCone(glLibObj):
    def __init__(self,radius,length,detail):
        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)
        Cylinder = gluNewQuadric()
        gluCylinder(Cylinder,radius,0.0,length,detail,1)
        glEndList()
class glLibObjTexCone(glLibObj):
    def __init__(self,radius,length,detail):
        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)
        Cylinder = gluNewQuadric()
        gluQuadricTexture(Cylinder,GLU_TRUE)
        gluCylinder(Cylinder,radius,0.0,length,detail,1)
        glEndList()
def GetNormal(t1,t2,t3,flip=False):
    v1 = [t2[0]-t1[0],t2[1]-t1[1],t2[2]-t1[2]]
    v2 = [t3[0]-t1[0],t3[1]-t1[1],t3[2]-t1[2]]
    vx = (v1[1] * v2[2]) - (v1[2] * v2[1])
    vy = (v1[2] * v2[0]) - (v1[0] * v2[2])
    vz = (v1[0] * v2[1]) - (v1[1] * v2[0])
    n = [vx, vy, vz]
    if flip:
        n = [-n[0],-n[1],-n[2]]
    return n
class glLibObjMap(glLibObj):
    def __init__(self,mapdata,texturing=False,normals=None,heightscalar=1.0):
        texturemap = []
        normalmap = []
        for z in xrange(len(mapdata)):
            normalrow = []
            texturerow = []
            for x in xrange(len(mapdata[0])):
                if normals == GLLIB_VERTEX_NORMALS:
                    Normals = []
                    t = 0
                    flip = True
                    leftpoint = rightpoint = uppoint = downpoint = False
                    normalpoint = (x,  heightscalar*mapdata[z  ][x  ],z  )
                    if x-1 >= 0:                 leftpoint   = (x-1,heightscalar*mapdata[z  ][x-1],z  )#; print "leftpoint", leftpoint
                    if x+1 <= len(mapdata[0])-1: rightpoint  = (x+1,heightscalar*mapdata[z  ][x+1],z  )#; print "rightpoint", rightpoint
                    if z+1 <= len(mapdata)-1:    uppoint     = (x,  heightscalar*mapdata[z+1][x  ],z+1)#; print "uppoint", uppoint
                    if z-1 >= 0:                 downpoint   = (x,  heightscalar*mapdata[z-1][x  ],z-1)#; print "downpoint", downpoint
                    if rightpoint and uppoint:   Normals.append(GetNormal(normalpoint,rightpoint,uppoint,flip))
                    if uppoint and leftpoint:    Normals.append(GetNormal(normalpoint,uppoint,leftpoint,flip))
                    if leftpoint and downpoint:  Normals.append(GetNormal(normalpoint,leftpoint,downpoint,flip))
                    if downpoint and rightpoint: Normals.append(GetNormal(normalpoint,downpoint,rightpoint,flip))
                    xcomp = []; ycomp = []; zcomp = []
                    for n in Normals:
                        xcomp.append(n[0]);ycomp.append(n[1]);zcomp.append(n[2])
                    normal = (sum(xcomp)/len(xcomp),sum(ycomp)/len(ycomp),sum(zcomp)/len(zcomp))
                    l = sqrt((normal[0]**2)+(normal[1]**2)+(normal[2]**2))
                    normal = [normal[0]/l,normal[1]/l,normal[2]/l]
                    normalrow.append(normal)
                if texturing != False:
                    xtexcoord = float(x)/(len(mapdata[0])-1)
                    ytexcoord = float(z)/(len(mapdata)-1)
                    texturerow.append((xtexcoord,ytexcoord))
            normalmap.append(normalrow)
            texturemap.append(texturerow)
        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)
        alreadytexturing = glGetBooleanv(GL_TEXTURE_2D)
        if texturing:
            glLibSelectTexture(texturing)
        glBegin(GL_QUADS)
        for z in xrange(len(mapdata)-1):
            zrow1 = mapdata[z-1]
            zrow2 = mapdata[z-1+1]
            for x in xrange(len(zrow1)-1):
                if normals == GLLIB_FACE_NORMALS:
                    Normals = []
                    Normals.append(GetNormal((x,  heightscalar*mapdata[z-1  ][x-1  ],z  ),(x,  heightscalar*mapdata[z-1+1][x-1  ],z+1),(x+1,heightscalar*mapdata[z-1  ][x-1+1],z  )))
                    Normals.append(GetNormal((x,  heightscalar*mapdata[z-1+1][x-1  ],z+1),(x+1,heightscalar*mapdata[z-1+1][x-1+1],z+1),(x,  heightscalar*mapdata[z-1  ][x-1  ],z  )))
                    Normals.append(GetNormal((x+1,heightscalar*mapdata[z-1  ][x-1+1],z  ),(x,  heightscalar*mapdata[z-1  ][x-1  ],z  ),(x+1,heightscalar*mapdata[z-1+1][x-1+1],z+1)))
                    Normals.append(GetNormal((x+1,heightscalar*mapdata[z-1+1][x-1+1],z+1),(x+1,heightscalar*mapdata[z-1  ][x-1+1],z  ),(x,  heightscalar*mapdata[z-1+1][x-1  ],z+1)))
                    xcomp = []; ycomp = []; zcomp = []
                    for n in Normals:
                        xcomp.append(n[0]);ycomp.append(n[1]);zcomp.append(n[2])
                    normal = (sum(xcomp)/4.0,sum(ycomp)/4.0,sum(zcomp)/4.0)
                    l = sqrt((normal[0]**2)+(normal[1]**2)+(normal[2]**2))
                    normal = [normal[0]/l,normal[1]/l,normal[2]/l]
                    glNormal3f(*normal)
                if normals == GLLIB_VERTEX_NORMALS: glNormal3f(*normalmap[z-1  ][x-1  ])
                if texturing: glTexCoord2f(*texturemap[z  ][x  ])
                glVertex3f(x,  heightscalar*zrow1[x-1  ],z  )
                if normals == GLLIB_VERTEX_NORMALS: glNormal3f(*normalmap[z-1  ][x-1+1])
                if texturing: glTexCoord2f(*texturemap[z  ][x+1])
                glVertex3f(x+1,heightscalar*zrow1[x-1+1],z  )
                if normals == GLLIB_VERTEX_NORMALS: glNormal3f(*normalmap[z-1+1][x-1+1])
                if texturing: glTexCoord2f(*texturemap[z+1][x+1])
                glVertex3f(x+1,heightscalar*zrow2[x-1+1],z+1)
                if normals == GLLIB_VERTEX_NORMALS: glNormal3f(*normalmap[z-1+1][x-1  ])
                if texturing: glTexCoord2f(*texturemap[z+1][x  ])
                glVertex3f(x,  heightscalar*zrow2[x-1  ],z+1)
        glEnd()
        if alreadytexturing: glEnable(GL_TEXTURE_2D)
        glEndList()
