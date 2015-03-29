"""
 A simple Game nemed Flootmoion
 Developed by NicoBosshard <nico@bosshome.ch>

 http://www.nicobosshard.ch
"""
import sys, math, pygame, random, time
import control
from pygame.locals import *
from OpenGLLibrary import *

#control.main()
pygame.init()
random.seed(time.clock())
Screen = (800,600)
Cube_speed_z=0.1
GenerateNewArea_Schutzzeit=0
Window = glLibWindow(Screen,caption="Lighting Test")
View3D = glLibView3D((0,0,Screen[0],Screen[1]),45)
View3D.set_view()

glLibTexturing(True)

Camera = glLibCamera([0,0.5,6],[0,0,0])

glLibLighting(True)
Sun = glLibLight([0,20,20],Camera)
Sun.enable()

glLibColorMaterial(True) 

drawing = 0
Objects = [glLibObjCube(),glLibObjTeapot(),glLibObjSphere(64),glLibObjCylinder(0.5,1.0,64),glLibObjCone(0.5,1.8,64),glLibObjFromFile("ExamplesData/Tunnel.obj")]
BGround = glLibObjFromFile("ExamplesData/Tunnel.obj")
Player = glLibObjTexSphere(0.5,64,0,0,2)

Texture = glLibTexture("ExamplesData/fugu.png")
Cubes = []

for z in range(-110,-10,10):
    for x in range(-1,2):
        for y in range(-1,2):
            if(random.randint(0,100)>50):
                Cubes.append(glLibObjCube(0.5,x,y,z,0,0,Cube_speed_z,random.randint(150,255),random.randint(150,255),random.randint(150,255),255))

    

while True:
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_RETURN:
                drawing += 1
                if drawing == 6:
                    drawing = 0
            if event.key == K_a: Player.x+=-0.1
            if event.key == K_w: Player.y+=0.1
            if event.key == K_d: Player.x+=0.1
            if event.key == K_s: Player.y+=-0.1
    if   key[K_LEFT]: Camera.set_target_pos([-6,0.5,0])
    elif key[K_RIGHT]: Camera.set_target_pos([6,0.5,0])
    elif key[K_UP]: Camera.set_target_pos([0,6,2])
    elif key[K_DOWN]: Camera.set_target_pos([0,-6,2])
    else: Camera.set_target_pos([0,0.5,6])

    Camera.update()
            
    Window.clear()
    Camera.set_camera()
    Sun.draw()
##    glLibColor((255,255,255))
##    
##    glTranslated(1,1,1)
##    Objects[0].draw()
##    glLibColor((255,0,0))
##    glTranslated(0,0,0)
##    Objects[1].draw()
##    glTranslated(-1,-1,-1)
##    Objects[3].draw()
##    Objects[4].draw()

    glTranslated(-0.5,Player.y,5+Player.x+1)
    BGround.draw()
    glTranslated(-0.5,-Player.y,-5+Player.x+1)

    glTranslated(-0.5,Player.y,5+Player.x+10)
    BGround.draw()
    glTranslated(-0.5,-Player.y,-5+Player.x+10)

    GenerateNewArea=0
    Object_ID=-1
    for Cube in Cubes:
        Object_ID+=1
        glTranslated(Cube.x,Cube.y,Cube.z)
        glLibColor((Cube.r,Cube.g,Cube.b,Cube.a))
        Cube.draw()
        Cube.x+=Cube.speed_x
        Cube.y+=Cube.speed_y
        Cube.z+=Cube.speed_z
        glTranslated(-Cube.x,-Cube.y,-Cube.z)
        if(Cube.z>5):
            GenerateNewArea=Cube.z-100
            Cubes.pop(Object_ID)

    glTranslated(Player.x,Player.y,Player.z)
    glLibColor((255,255,255,255))
    Player.draw()
    glTranslated(-Player.x,-Player.y,-Player.z)
    
    Window.flip()

    GenerateNewArea_Schutzzeit-=1
    if(GenerateNewArea<0 and GenerateNewArea_Schutzzeit<1):
        GenerateNewArea_Schutzzeit=20
        for x in range(-1,2):
            for y in range(-1,2):
                if(random.randint(0,100)>50):
                    Cubes.append(glLibObjCube(0.5,x,y,GenerateNewArea,0,0,Cube_speed_z,random.randint(150,255),random.randint(150,255),random.randint(150,255),255))
        
