"""
 A simple Game nemed Flootmoion
 Developed by NicoBosshard <nico@bosshome.ch>

 http://www.nicobosshard.ch
"""
import sys, math, pygame, random
from operator import itemgetter

from graphics import *

class CreateCube:
    def __init__(self, win_width = 1024, win_height = 600):
        pygame.init()

        self.screen = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption("Flootmotion V0.1")
        
        self.clock = pygame.time.Clock()

        self.vertices = [
            Point3D(-1,1,-1),
            Point3D(1,1,-1),
            Point3D(1,-1,-1),
            Point3D(-1,-1,-1),
            Point3D(-1,1,1),
            Point3D(1,1,1),
            Point3D(1,-1,1),
            Point3D(-1,-1,1)
        ]


        # Define the vertices that compose each of the 6 faces. These numbers are
        # indices to the vertices list defined above.
        self.faces  = [(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(0,4,5,1),(3,2,6,7)]

        # Define colors for each face
        self.colors = [(random.randint(0,255),random.randint(0,255),random.randint(0,255)),(random.randint(0,255),random.randint(0,255),random.randint(0,255)),(random.randint(0,255),random.randint(0,255),random.randint(0,255)),(random.randint(0,255),random.randint(0,255),random.randint(0,255)),(random.randint(0,255),random.randint(0,255),random.randint(0,255)),(random.randint(0,255),random.randint(0,255),random.randint(0,255))]

        self.angle = 0
        

def run(self):
    """ Main Loop """
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        self.clock.tick(50)
        self.screen.fill((0,32,0))

        # It will hold transformed vertices.
        t = []
        
        for v in self.vertices:
            v.x=v.x+0.005
            #v.y=v.y-0.00005
            v.z=v.z+random.randint(0,1)/100
            # Rotate the point around X axis, then around Y axis, and finally around Z axis.
            r = v.rotateX(self.angle).rotateY(self.angle).rotateZ(self.angle)
            # Transform the point from 3D to 2D
            p = r.project(self.screen.get_width(), self.screen.get_height(), 256, 4)
            # Put the point in the list of transformed vertices
            t.append(p)

        # Calculate the average Z values of each face.
        avg_z = []
        i = 0
        for f in self.faces:
            z = (t[f[0]].z + t[f[1]].z + t[f[2]].z + t[f[3]].z) / 4.0
            avg_z.append([i,z])
            i = i + 1

        # Draw the faces using the Painter's algorithm:
        # Distant faces are drawn before the closer ones.
        for tmp in sorted(avg_z,key=itemgetter(1),reverse=True):
            face_index = tmp[0]
            f = self.faces[face_index]
            pointlist = [(t[f[0]].x, t[f[0]].y), (t[f[1]].x, t[f[1]].y),
                         (t[f[1]].x, t[f[1]].y), (t[f[2]].x, t[f[2]].y),
                         (t[f[2]].x, t[f[2]].y), (t[f[3]].x, t[f[3]].y),
                         (t[f[3]].x, t[f[3]].y), (t[f[0]].x, t[f[0]].y)]
            pygame.draw.polygon(self.screen,self.colors[face_index],pointlist)

            
        self.angle += 1
        
        pygame.display.flip()

        if(self.angle==200):
            AAA=CreateCube()
            print AAA.faces
            run(AAA)

if __name__ == "__main__":
    AAA=CreateCube()
    print AAA.faces
    run(AAA)
    #Simulation().run()
    #Simulation().run()
