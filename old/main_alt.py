"""
 A simple Game nemed Flootmoion
 Developed by NicoBosshard <nico@bosshome.ch>

 http://www.nicobosshard.ch

 Required numpy and pygame to be installed or copy in this Folder. I don't put them into the installer because this is only experimentl Code.
"""

import sys, math, pygame, random
from operator import itemgetter

from graphics import *

class CreateCube:
    def __init__(self, posx, posy, posz = -20, win_width = 1024, win_height = 600):
        pygame.init()

        self.screen = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption("Flootmotion V0.1")
        
        self.clock = pygame.time.Clock()

        #posx=0
        #posy=1
        posz=random.randint(50,50)


        self.vertices = [
            Point3D(-0.5+posx,0.5+posy,-0.5+posz),
            Point3D(0.5+posx,0.5+posy,-0.5+posz),
            Point3D(0.5+posx,-0.5+posy,-0.5+posz),
            Point3D(-0.5+posx,-0.5+posy,-0.5+posz),
            Point3D(-0.5+posx,0.5+posy,0.5+posz),
            Point3D(0.5+posx,0.5+posy,0.5+posz),
            Point3D(0.5+posx,-0.5+posy,0.5+posz),
            Point3D(-0.5+posx,-0.5+posy,0.5+posz)
        ]



        # Define the vertices that compose each of the 6 faces. These numbers are
        # indices to the vertices list defined above.
        self.faces  = [(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(0,4,5,1),(3,2,6,7)]

        # Define colors for each face
        self.colors = [(random.randint(50,255),random.randint(50,255),random.randint(50,255)),(random.randint(50,255),random.randint(0,255),random.randint(0,255)),(random.randint(50,255),random.randint(0,255),random.randint(0,255)),(random.randint(50,255),random.randint(0,255),random.randint(0,255)),(random.randint(50,255),random.randint(0,255),random.randint(0,255)),(random.randint(50,255),random.randint(0,255),random.randint(0,255))]

        self.angle = 0

        
        for i in range(8):
            self.vertices[i] = self.vertices[i].rotateX(1).rotateY(1).rotateZ(1)

def CreateBarrier(zeilen, spalten):
    for ix in range(zeilen):
        for iy in range(spalten):
            Cubes.append(CreateCube(ix,iy))
        

def run():
    """ Main Loop """
    Cubes=[]
##    Cubes.append(CreateCube(-1.5,-1.5))
##    Cubes.append(CreateCube(0,-1.5))
##    Cubes.append(CreateCube(1.5,-1.5))
##    
##    Cubes.append(CreateCube(-1.5,0))
##    Cubes.append(CreateCube(0,0,-10))
##    Cubes.append(CreateCube(1.5,0))
##    
##    Cubes.append(CreateCube(-1.5,1.5))
##    Cubes.append(CreateCube(0,1.5))
##    Cubes.append(CreateCube(1.5,1.5))


    for i in range(5):
        #Cubes.append(CreateCube(random.uniform(-1.5,1.5),random.uniform(-1.5,1.5)))
        Cubes.append(CreateCube(random.randint(-1,1),random.randint(-1,1)))
    
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        Object_ID=0
        
        for Cube in Cubes:
            Cube.screen.fill((0,32,0))
            if Cube.vertices[0].z<-3:
                Cubes.pop(Object_ID)
                #Cubes.append(CreateCube(random.uniform(-1.5,1.5),random.uniform(-1.5,1.5)))
                Cubes.append(CreateCube(random.randint(-1,1),random.randint(-1,1)))
                #print "delete"
            else:
                Object_ID += 1

        for Cube in Cubes:
            Cube.clock.tick(500)
            

            # It will hold transformed vertices.
            t = []
            
            for v in Cube.vertices:
                #v.x=v.x+0.005
                #v.y=v.y-0.00005
                #v.z=v.z+random.randint(0,1)/100
                v.z=v.z-0.2
                # Rotate the point around X axis, then around Y axis, and finally around Z axis.
                #r = v.rotateX(Cube.angle).rotateY(Cube.angle).rotateZ(Cube.angle)
                #r=v.rotateZ(Cube.angle)
                #v=v.rotateX(Cube.angle)
                r=v
                #r=v
                # Transform the point from 3D to 2D
                p = r.project(Cube.screen.get_width(), Cube.screen.get_height(), 256, 4)
                # Put the point in the list of transformed vertices
                t.append(p)

            # Calculate the average Z values of each face.
            avg_z = []
            i = 0
            for f in Cube.faces:
                z = (t[f[0]].z + t[f[1]].z + t[f[2]].z + t[f[3]].z) / 4.0
                avg_z.append([i,z])
                i = i + 1

            #print avg_z
            # Draw the faces using the Painter's algorithm:
            # Distant faces are drawn before the closer ones.
            for tmp in sorted(avg_z,key=itemgetter(1),reverse=True):
                face_index = tmp[0]
                f = Cube.faces[face_index]
                pointlist = [(t[f[0]].x, t[f[0]].y), (t[f[1]].x, t[f[1]].y),      
                             (t[f[1]].x, t[f[1]].y), (t[f[2]].x, t[f[2]].y),
                             (t[f[2]].x, t[f[2]].y), (t[f[3]].x, t[f[3]].y),
                             (t[f[3]].x, t[f[3]].y), (t[f[0]].x, t[f[0]].y)]
                pygame.draw.polygon(Cube.screen,Cube.colors[face_index],pointlist)
                #print pointlist


                
            Cube.angle += random.random()

            #if v.z<0:
            #    Cubes.remove(0)
            #else:
            #    Object_ID += 1
                
        
        pygame.display.flip()
        #input()

        #if(Cube.angle==200):
            #AAA=CreateCube()
            #print AAA.faces
            #Cubes.append(AAA,0,0)

if __name__ == "__main__":
    AAA=CreateCube(0,0)
    print AAA.faces
    run()
    #Simulation().run()
    #Simulation().run()
