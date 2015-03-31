import pygame
import pygame.gfxdraw
#import psyco
import numpy
import math
import random

#psyco.full()

s_w,s_h = 150,100
r_w,r_h = 400,300
pygame.screen = s = pygame.display.set_mode([r_w,r_h],pygame.DOUBLEBUF)
clock = pygame.time.Clock()
pygame.surf = pygame.Surface([s_w,s_h])
pygame.arr = pygame.surfarray.pixels3d(pygame.surf)
#pygame.display.set_mode((640,480),pygame.FULLSCREEN)

def load_tex(img):
    tex = pygame.image.load(img)
    
    texarr = []
    mem = []
    alpha = 255
    for z in range(50):
        blank = tex.convert()
        blank.fill([0,0,0])
        tex.set_alpha(alpha)
        blank.blit(tex,[0,0])
        alpha = int(0.96*alpha)
        arr = pygame.surfarray.pixels3d(blank)
        texarr.append(arr)
        mem.append(blank)
    tw = tex.get_width()-1
    th = tex.get_height()-1
    return texarr,mem,tw,th
    
texarr,mem,tw,th = load_tex("bm.bmp")

def trans(q,x=0,y=0,z=0):
    for p in q[:4]:
        p[0]+=x
        p[1]+=y
        p[2]+=z
def push(q,z=0):
    q[0][2]+=z
    q[3][2]+=z
def uvscroll(q,u=0,v=0):
    for p in q[:4]:
        p[3]+=u
        p[4]+=v

class Quad:
    def __init__(self,points,color,texture=texarr):
        self.points = points
        self.color = color
        self.texture = texture
        self.calc_corners()
    def calc_corners(self):
        self.corners = []
        for p in self.points:
            tp = self.trans(p)
            self.corners.append(tp)
    def trans(self,p):
        x,y,z,u,v = p
        z = float((z*1.0/300.0)+1)
        if z==0:
            z=0.1
        d = s_w
        x = (d*x/float(r_w))/z
        x+=s_w//2
        d = s_h
        y = (d*y/float(r_w))/z
        y+=s_h//2
        return [x,y,z,u,v]
    def rot(self,rx=0,ry=0,rz=0,center=[0,0,0]):
        for q in self.points:
            x,y,z = q[:3]
            cx,cy,cz = center[:3]
            x=x-cx
            y=y-cy
            z=z-cz
            if rx:
                theta = rx*math.pi/180.0
                s,c = math.sin(theta),math.cos(theta)
                y = y*c-z*s
                z = y*s+z*c
                x = x
            if ry:
                theta = ry*math.pi/180.0
                s,c = math.sin(theta),math.cos(theta)
                z = z*c-x*s
                x = z*s+x*c
                y = y
            if rz:
                theta = rz*math.pi/180.0
                s,c = math.sin(theta),math.cos(theta)
                x = x*c-y*s
                y = x*s+y*c
                z = z
            q[0]=x+cx
            q[1]=y+cy
            q[2]=z+cz
    def __getitem__(self,k):
        return self.points[k]
quad = Quad([[0,0,0,0,0],
            [140,0,0,1,0],
            [140,140,0,1,1],
            [0,140,0,0,1]],
            [255,255,255])
quad2 = Quad([[0,0,140,0,0],
            [140,0,140,1,0],
            [140,140,140,1,1],
            [0,140,140,0,1]],
            [255,0,0])
quad3 = Quad([[0,0,0,0,0],
            [0,0,140,1,0],
            [0,140,140,1,1],
            [0,140,0,0,1]],
            [0,255,0])
quad4 = Quad([[0,0,0,0,0],
            [0,0,140,1,0],
            [0,140,140,1,1],
            [0,140,0,0,1]],
            [0,255,0])
trans(quad4,x=140)
quads = [quad,quad2,quad3,quad4]
odepth = [1000 for i in range(s_w*s_h)]
pygame.depth = odepth[:]

def draw_point(x,y,z,u,v,color=None):
    pygame.points += 1
    #z = 0 to 1
    #want z = 0 to 400
    #z/z`=140/20
    #z = 140/20*z`
    z = float((z*1.0/300)+1)
    if z<=0:
        return
    #x = 0 to s_w
    #x = 0 to r_w
    x = (x*s_w/float(r_w))/z+s_w//2
    y = (y*s_w/float(r_w))/z+s_h//2
    x,y = int(x),int(y)
    if x<0 or x>=s_w or y<0 or y>=s_h:
        return
    if pygame.depth[y*s_w+x]<z:
        return
    pygame.depth[y*s_w+x] = z
    if not color:
        color = arr[int(u*(tex.get_width()-1)),int(v*(tex.get_height()-1))]
        #~ color = [int(color[0]/z),int(color[1]/z),int(color[2]/z)]
    pygame.arr[x,y] = color

def draw_line(s,e,color):
    line = [s,e]
    x,y,z,u,v = line[0]
    steps = 100
    xs = (line[1][0]-line[0][0])/float(steps)
    ys = (line[1][1]-line[0][1])/float(steps)
    zs = (line[1][2]-line[0][2])/float(steps)
    us = (line[1][3]-line[0][3])/float(steps)
    vs = (line[1][4]-line[0][4])/float(steps)
    for i in range(steps):
        draw_point(x,y,z,u,v)
        x+=xs
        y+=ys
        z+=zs
        u+=us
        v+=vs

grey = numpy.array([100,100,100],dtype=numpy.uint8)
def draw_point2(x,y,z,u,v,texture):
    pygame.points += 1
    if x<0 or x>=s_w:
        return
    if y<0 or y>=s_h:
        return
    if z<=0:
        return
    if pygame.depth[y*s_w+x]<z:
        return
    pygame.depth[y*s_w+x] = z
    #~ u+=random.random()*z/100.0
    #~ v+=random.random()*z/100.0
    #~ if u>1: u-=1
    #~ if u<0: u+=1
    #~ if v>1: v-=1
    #~ if v<0: v+=1
    #~ z = max(1,int(z))
    #~ z = min(4,z)
    color = texture[int(z*10)][int(u%1*tw),int(v%1*th)]
    pygame.arr[x,y] = color
    
def draw_hline(x1,y1,z1,u1,v1,x2,y2,z2,u2,v2):
    x,y,z,u,v = x1,y1,z1,u1,v1
    w = abs(x2-x1)
    if not w:
        return
    dx = (x2-x1)/w
    dy = 0
    dz = (z2-z1)/w
    du = (u2-u1)/w
    dv = 0
    while 1:
        draw_point2(int(x),int(y),z,u,v)
        x+=dx
        z+=dz
        u+=du
        if x2>x1 and x>x2:
            break
        if x2<x1 and x<x2:
            break
            
def draw_tri_bottom(a,b,c):
    """draw triangle"""
    y = min([a[1],b[1],c[1]])
    x,y,z,u,v = a
    w = abs(b[0]-a[0])
    va = "x"
    if w==0:
        w = abs(b[1]-a[1])
        va = "y"
    if w==0:
        return
    dx = (b[0]-a[0])/w
    dy = (b[1]-a[1])/w
    dz = (b[2]-a[2])/w
    du = (b[3]-a[3])/w
    dv = (b[4]-a[4])/w
    while 1:
        if va=="x":
            if dx>0 and x>=b[0]:
                break
            if dx<0 and x<=b[0]:
                break
        if va=="y":
            if dy>0 and y>=b[1]:
                break
            if dy<0 and y<=b[1]:
                break
        draw_line2(x,y,z,u,v,*c)
        x+=dx
        y+=dy
        z+=dz
        u+=du
        v+=dv

def draw_line2(x1,y1,z1,u1,v1,x2,y2,z2,u2,v2):
    x,y,z,u,v = x1,y1,z1,u1,v1
    w = abs(x2-x1)
    if not w:
        return
    dx = (x2-x1)/w
    dy = (y2-y1)/w
    dz = (z2-z1)/w
    du = (u2-u1)/w
    dv = (v2-v1)/w
    while 1:
        draw_point2(int(x),int(y),z,u,v)
        x+=dx
        y+=dy
        z+=dz
        u+=du
        v+=dv
        if x2>x1 and x>x2:
            break
        if x2<x1 and x<x2:
            break
            
def draw_tri2(a,b,c):
    """draw triangle with diagonal lines from one point to
    the two other points"""
    x,y,z,u,v = a
    w = abs(b[0]-a[0])
    va = "x"
    if w==0:
        w = abs(b[1]-a[1])
        va = "y"
    if w==0:
        return
    dx = (b[0]-a[0])/w
    dy = (b[1]-a[1])/w
    dz = (b[2]-a[2])/w
    du = (b[3]-a[3])/w
    dv = (b[4]-a[4])/w
    while 1:
        if va=="x":
            if dx>0 and x>=b[0]:
                break
            if dx<0 and x<=b[0]:
                break
        if va=="y":
            if dy>0 and y>=b[1]:
                break
            if dy<0 and y<=b[1]:
                break
        draw_line2(x,y,z,u,v,*c)
        x+=dx
        y+=dy
        z+=dz
        u+=du
        v+=dv
        
def draw_tri3(a,b,c,texture):
    """draws triangle with horizontal lines"""
    #Sort points vertically
    a,b,c = sorted([a,b,c],key=lambda t: t[1])
    #upside down triangle with flat top
    if a[1]==b[1]:
        draw_tri_point_down(a,b,c,texture)
        return
    #triangle with flat bottom
    if b[1]==c[1]:
        draw_tri_point_up(a,b,c,texture)
        return
    #triangle should be split
    else:
        draw_tri_split(a,b,c,texture)
        
def draw_tri_split(a,b,c,texture):
    """Split a rotated triangle into an upward and downward pointing one"""
    d = [0,b[1],0,0,0]
    if c[0]==a[0]:
        d[0] = c[0]
    else:
        m = (c[1]-a[1])/(c[0]-a[0])
        i=a[1]-m*a[0]
        d[0] = (d[1]-i)/m
    if c[2]==a[2]:
        d[2] = c[2]
    else:
        m = (c[1]-a[1])/(c[2]-a[2])
        i=a[1]-m*a[2]
        d[2] = (d[1]-i)/m
    if c[3]==a[3]:
        d[3] = c[3]
    else:
        m = (c[1]-a[1])/(c[3]-a[3])
        i=a[1]-m*a[3]
        d[3] = (d[1]-i)/m
    if c[4]==a[4]:
        d[4] = c[4]
    else:
        m = (c[1]-a[1])/(c[4]-a[4])
        i=a[1]-m*a[4]
        d[4] = (d[1]-i)/m
    draw_tri_point_up(a,b,d,texture)
    draw_tri_point_down(b,d,c,texture)
    
def draw_line3(x1,y1,z1,u1,v1,x2,y2,z2,u2,v2,texture):
    """horizontal"""
    x,y,z,u,v = x1,y1,z1,u1,v1
    w = abs(x2-x1)
    if not w:
        return
    if y<0 or y>=s_h:
        return
    dx = 1
    dy = 0
    dz = (z2-z1)/w
    du = (u2-u1)/w
    dv = (v2-v1)/w
    while x<x2:
        if x>=s_w:
            return
        if x>=0:
            draw_point2(int(x),int(y),z,u,v,texture)
        x+=dx
        y+=dy
        z+=dz
        u+=du
        v+=dv

def draw_tri_point_up(a,b,c,texture):
    """flat bottom"""
    b,c = sorted([b,c],key=lambda t: t[0])
    x,y,z,u,v = a
    ex,ey,ez,eu,ev = a
    if c[0]<b[0]:
        b,c = c,b
    ydist = float(b[1]-y)
    dx1 = (b[0]-x)/ydist
    dx2 = (c[0]-ex)/ydist
    dy1 = 1
    dy2 = 1
    dz1 = (b[2]-z)/ydist
    dz2 = (c[2]-ez)/ydist
    du1 = (b[3]-u)/ydist
    du2 = (c[3]-eu)/ydist
    dv1 = (b[4]-v)/ydist
    dv2 = (c[4]-ev)/ydist
    while y<=b[1]:
        draw_line3(x,y,z,u,v,ex,ey,ez,eu,ev,texture)
        x+=dx1
        y+=dy1
        z+=dz1
        u+=du1
        v+=dv1
        ex+=dx2
        ey+=dy2
        ez+=dz2
        eu+=du2
        ev+=dv2

def draw_tri_point_down(a,b,c,texture):
    """flat top"""
    if b[0]<a[0]:
        b,a = a,b
    x,y,z,u,v = a
    ex,ey,ez,eu,ev = b
    ydist = float(c[1]-y)
    dx1 = (c[0]-x)/ydist
    dx2 = (c[0]-ex)/ydist
    dy1 = 1
    dy2 = 1
    dz1 = (c[2]-z)/ydist
    dz2 = (c[2]-ez)/ydist
    du1 = (c[3]-u)/ydist
    du2 = (c[3]-eu)/ydist
    dv1 = (c[4]-v)/ydist
    dv2 = (c[4]-ev)/ydist
    while y<=c[1]:
        draw_line3(x,y,z,u,v,ex,ey,ez,eu,ev,texture)
        x+=dx1
        y+=dy1
        z+=dz1
        u+=du1
        v+=dv1
        ex+=dx2
        ey+=dy2
        ez+=dz2
        eu+=du2
        ev+=dv2
        
def draw_quad2(q):
    """Draws a quad sample in screen space"""
    q.calc_corners()
    ul = q.corners[0]
    ur = q.corners[1]
    br = q.corners[2]
    bl = q.corners[3]
    draw_tri3(ul,ur,br,q.texture)
    draw_tri3(ul,br,bl,q.texture)
    

def draw_quad1(q):
    """Draws a quad by sampling in polygon space across and down"""
    color = q.color
    #march start from q[0] to q[1]
    #march end from q[3] to q[2]
    x1 = q[0][0]
    y1 = q[0][1]
    z1 = q[0][2]
    u1 = q[0][3]
    v1 = q[0][4]
    x2 = q[3][0]
    y2 = q[3][1]
    z2 = q[3][2]
    u2 = q[3][3]
    v2 = q[3][4]
    xw1 = q[1][0]-q[0][0]
    yw1 = q[1][1]-q[0][1]
    zw1 = q[1][2]-q[0][2]
    uw1 = q[1][3]-q[0][3]
    vw1 = q[1][4]-q[0][4]
    xw2 = q[2][0]-q[3][0]
    yw2 = q[2][1]-q[3][1]
    zw2 = q[2][2]-q[3][2]
    uw2 = q[2][3]-q[3][3]
    vw2 = q[2][4]-q[3][4]
    w = float(max([abs(x) for x in [xw1,zw1,xw2,zw2]]))
    #sample based on average distance
    az = ((q[0][2]+q[1][2]+q[2][2]+q[3][2])/140.0+2)
    if az<=0:
        return
    d1 = [x/w for x in [xw1,yw1,zw1,uw1,vw1]]
    d2 = [x/w for x in [xw2,yw2,zw2,uw2,vw2]]
    p1 = [x1,y1,z1,u1,v1]
    p2 = [x2,y2,z2,u2,v2]
    while w>0:
        draw_line(p1,p2,color)
        w-=1
        for i in range(5):
            p1[i]+=d1[i]
            p2[i]+=d2[i]

def main():
    next_update = 1
    draw_quad = draw_quad2
    running = 1
    while running:
        dt = clock.tick(200)
        pygame.display.set_caption("%s"%clock.get_fps())
        pygame.points = 0
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                running = 0
            #~ if e.type==pygame.KEYDOWN and e.key==pygame.K_1:
                #~ draw_line3 = draw_line3_inline
            #~ if e.type==pygame.KEYDOWN and e.key==pygame.K_2:
                #~ draw_line3 = draw_line3_func
        keys = pygame.key.get_pressed()
        spd = 5
        if keys[pygame.K_a]:
            [trans(quad,z=-spd) for quad in quads]
        if keys[pygame.K_z]:
            [trans(quad,z=spd) for quad in quads]
        if keys[pygame.K_LEFT]:
            [trans(quad,x=-spd) for quad in quads]
        if keys[pygame.K_RIGHT]:
            [trans(quad,x=spd) for quad in quads]
        if keys[pygame.K_UP]:
            [trans(quad,y=-spd) for quad in quads]
        if keys[pygame.K_DOWN]:
            [trans(quad,y=spd) for quad in quads]
        if keys[pygame.K_r]:
            [q.rot(ry=1,center=quads[0][0]) for q in quads]
        if keys[pygame.K_t]:
            [q.rot(rx=1,center=quads[0][0]) for q in quads]
        if keys[pygame.K_y]:
            [q.rot(rz=1,center=quads[0][0]) for q in quads]
        if keys[pygame.K_f]:
            [q.rot(-1,center=quads[0][0]) for q in quads]
        uvscroll(quads[0],u=0,v=.01)
        if next_update<0:
            [quad.calc_corners() for quad in quads]
            next_update = 0#100
            pygame.depth = odepth[:]
            pygame.surf.fill([0,0,0])
            [draw_quad(q) for q in quads]
            surf = pygame.transform.scale(pygame.surf,[r_w,r_h])
            pygame.screen.blit(surf,[0,0])
        next_update -= dt
        pygame.display.flip()

#~ import cProfile as profile
#~ profile.run("main()")
main()
