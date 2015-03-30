"""
 A simple Game nemed Flootmoion
 Developed by NicoBosshard <nico@bosshome.ch>

 http://www.nicobosshard.ch
"""
import Leap, sys, thread, math, pygame, random, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from pygame.locals import *
from OpenGLLibrary import *

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
pygame.mixer.music.load("235349__dambient__8-bit-loop.mp3")
pygame.mixer.music.play()
##pygame.mixer.music.loop()

Camera_pos = [0,0.5,6]

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        #print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              #frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            print "  %s, id %d, position: %s" % (
                handType, hand.id, hand.palm_position)

            Player.speed_x=(hand.palm_position[0]/30-Player.x)/10
            Player.speed_y=(hand.palm_position[1]/30-8-Player.y)/10
            Player.speed_z=(hand.palm_position[2]/30-Player.z)/10

            print Player.speed_x
            print Player.speed_y
            print Player.speed_z


listener = SampleListener()
controller = Leap.Controller()

controller.add_listener(listener)

frame = controller.frame()



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
    if key[K_a]: Player.x+=-0.04
    if key[K_w]: Player.y+=0.04
    if key[K_d]: Player.x+=0.04
    if key[K_s]: Player.y+=-0.04
##    if   key[K_LEFT]: Camera.set_target_pos([-6,0.5,0])
##    elif key[K_RIGHT]: Camera.set_target_pos([6,0.5,0])
##    elif key[K_UP]: Camera.set_target_pos([0,6,2])
##    elif key[K_DOWN]: Camera.set_target_pos([0,-6,2])
##    else: Camera.set_target_pos([0,0.5,6])
    if key[K_LEFT]: Camera_pos[0]-=1
    if key[K_RIGHT]: Camera_pos[0]+=1
    if key[K_UP]: Camera_pos[2]-=1
    if key[K_DOWN]: Camera_pos[2]+=1
    if key[K_0]: Camera_pos = [0,0.5,6]

    Camera.set_target_pos(Camera_pos)

    Player.x+=Player.speed_x
    Player.y+=Player.speed_y
    Player.z+=Player.speed_z

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

##    glTranslated(-0.5,Player.y,5+Player.x+1)
##    BGround.draw()
##    glTranslated(-0.5,-Player.y,-5+Player.x+1)
##
##    glTranslated(-0.5,Player.y,5+Player.x+10)
##    BGround.draw()
##    glTranslated(-0.5,-Player.y,-5+Player.x+10)

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



