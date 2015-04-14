"""
 A simple Game nemed Flootmoion
 Developed by NicoBosshard <nico@bosshome.ch>

 http://www.nicobosshard.ch

Known Bugs:
No Transparence by tintime generated Cubes

To-Do:
Sphere texture
    - damage texture
Sphere Rotation
"""
import Leap, sys, threading, math, pygame, random, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from pygame.locals import *
from OpenGLLibrary import *

#pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
#pygame.mixer.music.load("./sound/235349__dambient__8-bit-loop.mp3")
#pygame.mixer.music.play()
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


def SphereRectCollision(sphere, rect):
    sphereXDistance = abs(sphere.x - rect.x)
    sphereYDistance = abs(sphere.y - rect.y)
    sphereZDistance = abs(sphere.z - rect.z)

    if(sphereXDistance >= (rect.size + sphere.radius)): return 0
    if(sphereYDistance >= (rect.size + sphere.radius)): return 0
    if(sphereZDistance >= (rect.size + sphere.radius)): return 0

    if(sphereXDistance < (rect.size)): return 1
    if(sphereYDistance < (rect.size)): return 1
    if(sphereZDistance < (rect.size)): return 1

    cornerDistance_sq = (sphereXDistance - rect.size)**2 + (sphereYDistance - rect.size)**2 + (sphereYDistance - rect.size)**2

    return (cornerDistance_sq < (sphere.radius * sphere.radius))


listener = SampleListener()
controller = Leap.Controller()

controller.add_listener(listener)

frame = controller.frame()

pygame.init()
System_Icon = pygame.image.load("img/Cube.ico")
pygame.display.set_icon(System_Icon)
screen = pygame.display.set_mode((1280, 1024))
#Heart_img = pygame.image.load("img/heart_PNG685.png")
Heart_img = pygame.image.load("img/Leap.jpg")
imagerect = Heart_img.get_rect()
screen.blit(pygame.transform.scale(Heart_img, (1280, 1024)), (0, 0))
pygame.display.flip()

speed=1
frame_time=time.clock()
frame_time_alt=time.clock()
##while True:
##    frame_time=time.clock()
##    speed=(frame_time-frame_time_alt)*60
##    print speed
##    frame_time_alt=frame_time
##    time.sleep(0.1)
#print(time.clock()-AAA)
random.seed(time.clock())
Screen = (1280,1024)
Cube_speed_z=0.05
Transparence=200
r=0
GenerateNewArea_Schutzzeit=0
Window = glLibWindow(Screen,caption="Float Motion - Nico Bosshard")
View3D = glLibView3D((0,0,Screen[0],Screen[1]-100),45)
Statusbar = glLibView2D((0,Screen[1]-100,Screen[0],100),45)


glLibTexturing(True)

Camera = glLibCamera([0,0.5,6],[0,0,0])
Staturbar_Camera = glLibCamera([0,0,0],[0,0,1])

glLibLighting(False)
Sun = glLibLight([0,20,20],Camera)
Sun.enable()
Staturbar_Sun = glLibLight([0,20,20],Camera)
Staturbar_Sun.enable()

glLibShadowInit([[512,5]])

glLibColorMaterial(True)

drawing = 0
#Objects = [glLibObjCube(),glLibObjTeapot(),glLibObjSphere(64),glLibObjCylinder(0.5,1.0,64),glLibObjCone(0.5,1.8,64),glLibObjFromFile("obj/Tunnel.obj")]

#time.sleep(2)
#Font_ALGER_72 = pygame.font.Font(os.path.join("Fonts","ALGER.TTF"),72)
#Font_BSSYM7_72 = pygame.font.Font(os.path.join("Fonts","BSSYM7.TTF"),72)

#Level_Text = glLibObjText("Level 1",Font_ALGER_72,(255,128,50))

Player = glLibObjTexSphere(0.3,64,0,0,2)
Texture = glLibTexture("textures/Oak Ligh.bmp")
Statusbar_hearts = []
Cubes = []
Particles = []
Stars = []

BGround = glLibObjFromFile("obj/leer.obj")

Heart_obj = glLibObjFromFile("obj/Heart.obj")

#time.sleep(2)

#for v in Heart.list:
#    print v
#print Heart.list

Cubes_count=0
Hearts_count=0
for z in range(-110,-10,10):
    for x in range(-1,2):
        for y in range(-1,2):
            if(random.randint(0,100)>50):
                Cubes.append(glLibObjCube(0.5,x,y,z,0,0,Cube_speed_z,random.randint(100,255),random.randint(100,255),random.randint(100,255),Transparence,0))
                Cubes_count+=1
            else:
                if(random.randint(0,100)>80):
                    Cubes.append(glLibObjCube(0.5,x,y,z,0,0,Cube_speed_z,255,0,0,100,1))
                    Hearts_count+=1
                

#if(Cubes_count==9):

#glClearColor( 1, 1, 1, 1)

P=-40

glEnable(GL_DEPTH_TEST)
#glDisable(GL_DEPTH_TEST)

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

            #Screenshotspeicherungsfunktion
            if event.key == K_F5:
                while True:
                    try:pygame.image.load(time.strftime("%a, %d %b %Y %H-%M-%S", time.gmtime())+".png")
                    except:glLibSaveScreenshot(time.strftime("%a, %d %b %Y %H-%M-%S", time.gmtime())+".png");break
                    counter = 1
                    while True:
                        try:pygame.image.load(time.strftime("%a, %d %b %Y %H-%M-%S", time.gmtime())+" ("+str(counter)+").png")
                        except:glLibSaveScreenshot(time.strftime("%a, %d %b %Y %H-%M-%S", time.gmtime())+" ("+str(counter)+").png");break
                        counter += 1
                    break #Warscheinlich nutzlos aber für die Zukunft.

    if key[K_a]: Player.x+=-0.04
    if key[K_w]: Player.y+=0.04
    if key[K_d]: Player.x+=0.04
    if key[K_s]: Player.y+=-0.04

    if key[K_j]: Player.speed_x+=-0.001
    if key[K_i]: Player.speed_y+=0.001
    if key[K_l]: Player.speed_x+=0.001
    if key[K_k]: Player.speed_y+=-0.001
    if key[K_o]: Player.speed_z+=0.001
    if key[K_p]: Player.speed_z+=-0.001
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
    Staturbar_Camera.set_target_pos(Camera_pos)

    Player.x+=Player.speed_x*speed
    Player.y+=Player.speed_y*speed
    Player.z+=Player.speed_z*speed

    Camera.update()
    Staturbar_Camera.update()

    Window.clear()

    Statusbar.set_view()
    Staturbar_Camera.set_camera()
    Staturbar_Sun.draw()

    #P+=0.001
    #glTranslated(P,-1.5,0)
    
    #Level_Text.draw()

    #glDisable(GL_DEPTH_TEST)
    # store the projection matrix to restore later
    #glMatrixMode(GL_PROJECTION)
    #glPushMatrix()
    # load orthographic projection matrix
    #glLoadIdentity()
    #glOrtho(0, float(self.width),0, float(self.height), 0, 1)
    #far=8192
    #glOrtho(-1280/2.,1024/2.,-1024/2.,1280/2.,0,far)
    # reset modelview
    #glMatrixMode(GL_MODELVIEW)
    #glLoadIdentity()
    #glClear(GL_COLOR_BUFFER_BIT)

##    z=-6
##    n=100
##    glTranslatef(0,0.0,-z)
##    glBegin(GL_TRIANGLES)
##    glVertex3f(0.0,n,0.0)
##    glVertex3f(-n,-n,0)
##    glVertex3f(n,-n,0)
##    glEnd()

    Heart_obj.draw()

    for Statusbar_heart in Statusbar_hearts:

        #glRotatef(90,0,1,0)
        #glScalef(4,4,4);
        glTranslated(4,0,0)
        Heart_obj.draw()
        Level_Text.draw()

        #glTranslated(-Statusbar_heart.x,-Statusbar_heart.y,-Statusbar_heart.z)
        #glScalef(0.25,0.25,0.25);
        #glRotatef(-90,0,1,0)


    #glTranslated(-44,1.5,0)


    View3D.set_view()
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
##

    #BGround.x=-0.25
    #BGround.y=-0.25
    BGround.z+=0.01*speed
    glScalef(10,10,10);
    glTranslated(BGround.x,BGround.y,BGround.z)
    BGround.draw()
    glTranslated(-BGround.x,-BGround.y,-BGround.z)
    glScalef(0.1,0.1,0.1);


##    glTranslated(-0.5,Player.y,5+Player.x+10)
##    BGround.draw()
##    glTranslated(-0.5,-Player.y,-5+Player.x+10)

    GenerateNewArea=0
    Object_ID=-1
    for Cube in Cubes:
        Object_ID+=1
        if(Cube.z>5):
            GenerateNewArea=Cube.z-100
            Cubes.pop(Object_ID)
        if(SphereRectCollision(Player,Cube)==1):
            for i in range(int(round(300/speed))):
                x=random.uniform(-Cube_speed_z,Cube_speed_z)
                y=random.uniform(-Cube_speed_z,Cube_speed_z)
                z=random.uniform(-Cube_speed_z,Cube_speed_z)
                magnitude  = sqrt(x**2 + y**2 + z**2)
                Particles.append(glLibObjCube(0.06,Player.x,Player.y,Player.z+0.5,x/magnitude/random.uniform(25,35), y/magnitude/random.uniform(25,35), z/magnitude/random.uniform(25,35),Cube.r,Cube.g,Cube.b,Transparence,2,round(200/speed)))
            Cubes.pop(Object_ID)


    for Cube in Cubes:
        Cube.x+=Cube.speed_x*speed
        Cube.y+=Cube.speed_y*speed
        Cube.z+=Cube.speed_z*speed
        if(Cube.cube_type==1): #Herzz
            glTranslated(Cube.x,Cube.y-0.8,Cube.z+0.8)
            glRotatef(90,0,1,0)
            glScalef(0.5,0.5,0.5);
            glLibColor((255,0,0,255))
            Heart_obj.draw() #Wichtig: Herz vor Würfel da sonst unsichtbar
            glScalef(2,2,2);
            glRotatef(-90,0,1,0)
            glTranslated(-Cube.x,-Cube.y+0.8,-Cube.z-0.8)
            
        glTranslated(Cube.x,Cube.y,Cube.z)
        glLibColor((Cube.r,Cube.g,Cube.b,Cube.a))
        Cube.draw()
        glTranslated(-Cube.x,-Cube.y,-Cube.z)
        
        

    Object_ID=-1
    for Particle in Particles:
        Object_ID+=1
        Particle.x+=Particle.speed_x*speed
        Particle.y+=Particle.speed_y*speed
        Particle.z+=Particle.speed_z*speed
        glTranslated(Particle.x,Particle.y,Particle.z)
        glLibColor((Particle.r,Particle.g,Particle.b,Particle.a))
        Particle.draw()
        glTranslated(-Particle.x,-Particle.y,-Particle.z)
        Particle.time-=1
        if(Particle.time==0):
            Particles.pop(Object_ID)

    glLibColor((255,255,255,255))
    glTranslated(Player.x,Player.y,Player.z)
    #r+=sqrt(Player.speed_x**2 + Player.speed_y**2 + Player.speed_z**2)*100
    Player.rotate_x+=Player.speed_x*100
    Player.rotate_y+=Player.speed_y*100
    Player.rotate_z+=Player.speed_z*100
    #if not (Player.speed_x==0 and Player.speed_y==0 and Player.speed_z==0):
    glRotatef(Player.rotate_x,0,1,0)
    glRotatef(-Player.rotate_y,1,0,0)
    glRotatef(Player.rotate_z,1,0,0)
    #print Player.speed_x*10000
    Player.draw()
    glTranslated(-Player.x,-Player.y,-Player.z)
    #glTranslated(-Player.x,-Player.y,-Player.z)
    #glRotatef(-10,Player.x,Player.y,Player.z)


    frame_time=time.clock()
    speed=(frame_time-frame_time_alt)*60
    #print speed
    frame_time_alt=frame_time
    
    Window.flip()


    GenerateNewArea_Schutzzeit-=1
    if(GenerateNewArea<0 and GenerateNewArea_Schutzzeit<1):
        GenerateNewArea_Schutzzeit=3
        for x in range(-1,2):
            for y in range(-1,2):
                if(random.randint(0,100)>50):
                    Cubes.append(glLibObjCube(0.5,x,y,GenerateNewArea,0,0,Cube_speed_z,random.randint(100,255),random.randint(100,255),random.randint(100,255),Transparence))
                else:
                    if(random.randint(0,100)>80):
                        Cubes.append(glLibObjCube(0.5,x,y,GenerateNewArea,0,0,Cube_speed_z,255,0,0,100,1))
                        Hearts_count+=1


