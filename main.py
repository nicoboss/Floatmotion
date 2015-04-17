﻿"""
 A simple Game nemed Flootmoion
 Developed by NicoBosshard <nico@bosshome.ch>

 http://www.nicobosshard.ch

Known Bugs:
No Transparence by tintime generated Cubes

To-Do:
- End Screen
- Kollisions Sounds
- BossCube als Fenster Icon
- Überdenken der GameOver Sphere Textur
- Löscher unützer Files wie z.B. obj
- NSIS Installer
- Shadow
- Rename SampeListener
- Comments in Surce Code
- Start screen picture
- Sphere Texture
- F1 Hilfe
"""
import Leap, sys, threading, math, pygame, random, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from pygame.locals import *
from OpenGLLibrary import *

Sound=["./sound/Sound1.mp3","./sound/Sound2.mp3","./sound/Sound3.mp3"]
Sound_GameOver="./sound/GameOver.mp3"
Sound_LevelUp="./sound/LevelUp.mp3"

pygame.mixer.init(size=-16, channels=2, buffer=4096)
pygame.mixer.music.load(Sound[random.randint(0,2)]) #random.randint(1,2)
pygame.mixer.music.play(-1)

Camera_pos = [0,0.5,6]

Level=1
Leben=70
Player_Schutzzeit=0
Zeit=0
Startzeit=0

Leben_alt=0

Level_pos=0
Level_length=500
BossPrepare=False
BossScene=False

more_FPS=False


def GenerateCube(z=-100):
    Cubes_count=0
    Hearts_count=0
    for x in range(-1,2):
        for y in range(-1,2):
            if(random.randint(0,100)>40+Level*3):
                Cubes.append(glLibObjCube(0.5,x,y,z,0,0,Cube_speed_z[Level-1],random.randint(100,255),random.randint(100,255),random.randint(100,255),Transparence))
                Cubes_count+=1
            else:
                if(random.randint(0,100)>75+Level*2):
                    Cubes.append(glLibObjCube(0.5,x,y,z,0,0,Cube_speed_z[Level-1],255,0,0,100,1))
                    Hearts_count+=1

    if(Cubes_count==9):
        for i in range(9):
            Cubes.pop() #by Defult remove last Objekt
        Cubes_count-=9
        for x in range(-1,2):
            for y in range(-1,2):
                Cubes.append(glLibObjCube(0.5,x,y,z,0,0,Cube_speed_z[Level-1],255,0,0,100,1))
        Hearts_count+=9


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

##            print "  %s, id %d, position: %s" % (
##                handType, hand.id, hand.palm_position)

            Player.speed_x=(hand.palm_position[0]/30-Player.x)/(15*speed)
            Player.speed_y=(hand.palm_position[1]/30-8-Player.y)/(15*speed)
            Player.speed_z=(hand.palm_position[2]/30-Player.z)/(20*speed)

##            print Player.speed_x
##            print Player.speed_y
##            print Player.speed_z


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
screen = pygame.display.set_mode((1280, 720))
#Heart_img = pygame.image.load("img/heart_PNG685.png")
Heart_img = pygame.image.load("img/Leap.jpg")
imagerect = Heart_img.get_rect()
screen.blit(pygame.transform.scale(Heart_img, (1280, 720)), (0, 0))
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
Screen = (1280,720)
Cube_speed_z=[0.05,0.055,0.06,0.065,0.07,0.075,0.08,0.085,0.09,0.1]
Transparence=200
r=0
GenerateNewArea_Schutzzeit=0
Window = glLibWindow(Screen,False,System_Icon,"Float Motion - Nico Bosshard",False)
View3D = glLibView3D((0,0,Screen[0],Screen[1]-100),45)
Statusbar = glLibView3D((0,Screen[1]-100,Screen[0],100),45)


glLibTexturing(True)

Camera = glLibCamera([0,0.5,6],[0,0,0])
Staturbar_Camera = glLibCamera([0,0,0],[0,0,1])

glLibLighting(False)
Sun = glLibLight([0,20,20],Camera)
Sun.enable()
Staturbar_Sun = glLibLight([0,20,20],Camera)
Staturbar_Sun.enable()

#glLibShadowInit([[512,5]])

glLibColorMaterial(True)

drawing = 0
#Objects = [glLibObjCube(),glLibObjTeapot(),glLibObjSphere(64),glLibObjCylinder(0.5,1.0,64),glLibObjCone(0.5,1.8,64),glLibObjFromFile("obj/Tunnel.obj")]

#time.sleep(2)
Font_ALGER_42 = pygame.font.Font(os.path.join("Fonts","ALGER.TTF"),42)
Font_ALGER_100 = pygame.font.Font(os.path.join("Fonts","ALGER.TTF"),100)
#Font_WINGDNG2_100 = pygame.font.Font(os.path.join("Fonts","WINGDNG2.TTF"),100)

Pause_Text = glLibObjText("Pause",Font_ALGER_100,(255,255,0))
Pause_Ready = glLibObjText("Ready",Font_ALGER_100,(255,200,0))
Pause_GO = glLibObjText("GO",Font_ALGER_100,(0,255,0))

Death_Game = glLibObjText("Game",Font_ALGER_100,(200,250,70))
Death_Over = glLibObjText("Over",Font_ALGER_100,(255,220,60))

BossCube_Level = glLibObjText("Level",Font_ALGER_100,(255,200,0))
#BossCube_Up = glLibObjText("Up",Font_ALGER_100,(180,230,30))
BossCube_Up = glLibObjText("Up",Font_ALGER_100,(255,230,30))

Player = glLibObjTexSphere(0.3,64,0,0,2)
Player_Particles = []
Texture_Player = glLibTexture("textures/Oak Ligh.bmp")
Statusbar_hearts = []
Cubes = []
Particles = []
Stars = []
BossCube=glLibObjBossCube(3,0,0,-100,0,0,0.1,255,0,0,0,0,-1)
BossCube_Particles = []

BGround = glLibObjFromFile("obj/leer.obj")

Star_obj = glLibObjFromFile("obj/Star.obj")
Heart_obj = glLibObjFromFile("obj/Heart.obj")


#time.sleep(2)

#for v in Heart.list:
#    print v
#print Heart.list


for z in range(-110,-10,18-Level):
    GenerateCube(z)


for i in range(400):
    #Die follgenden if-Bedingungen sind zum verhindern von Sternen in der Würfelzone.
    if(random.randint(1,100)>50):
        Star_x=random.uniform(-20,-2)
    else:
        Star_x=random.uniform(2,20)

    if(random.randint(1,100)>50):
        Star_y=random.uniform(-20,-2)
    else:
        Star_y=random.uniform(2,20)

    Stars.append(glLibObjStar(random.uniform(0.01,0.03),Star_x,Star_y,random.uniform(-100,0),0,0,Cube_speed_z[Level-1],random.randint(100,255),random.randint(100,255),random.randint(100,255),Transparence,0))


#glClearColor( 1, 1, 1, 1)

P=-40

glLibTexturing(True)
glEnable(GL_DEPTH_TEST)
#glDisable(GL_DEPTH_TEST)

Level_Text = glLibObjText("Level "+str(Level),Font_ALGER_100,(255,200,0))
Lives_Text = glLibObjText("Lives "+str(Leben),Font_ALGER_100,(255,30,10))

Pause_Startzeit=0
Pause_Time=0
Startzeit=time.clock()


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
            

            #Pause Funktionn
            if event.key == K_PAUSE or event.key == K_SPACE:
                Pause_Startzeit=time.clock()

                #Der dept test wird temporär ausgeshaltet, dammit keine Würfel vor der Schrift gezeichnet werden können.
                glDisable(GL_DEPTH_TEST)
                glTranslated(-1.4,0.8,2)
                Pause_Text.draw()
                Window.flip()

                Flip_1or2=1

                no_continue_key_press=True
                while no_continue_key_press:
                    time.sleep(0.5)
                    for event_p in pygame.event.get():
                        if(event.type == KEYDOWN):
                            if(time.clock()-Pause_Startzeit>1):
                                no_continue_key_press=False
                                break
                    Window.flip()
                    Flip_1or2*=-1

                if(Flip_1or2==1):
                    Window.flip()

                glTranslated(-0.8,-0.7,0) #glTranslated(-1.4,0.8,2) und ergiebt glTranslated(-2.2,0.1,2)
                glScalef(1.5,1.5,1.5);

                Pause_Ready.draw()
                Window.flip()
                time.sleep(1)

                glScalef(2,2,2);
                glTranslated(0.2,-0.3,0)
                Pause_GO.draw()
                Window.flip()
                time.sleep(1)
                glTranslated(-0.2,0.3,0)
                glScalef(0.5,0.5,0.5);
                glTranslated(2.2,-0.1,-2)
                glEnable(GL_DEPTH_TEST)

                Pause_Time+=time.clock()-Pause_Startzeit
                frame_time_alt=time.clock()

            #More FPS Funkttion (no Stars)
            if event.key == K_F2:
                if(more_FPS==False):
                    more_FPS=True
                else:
                    more_FPS=False

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

            if event.key == K_x or event.key == K_PLUS or event.key == K_KP_PLUS:
                Level+=1
                if(Level<10):
                    Level_Text = glLibObjText("Level "+str(Level),Font_ALGER_100,(255,200,0))
                elif(Level==10):
                    Level_Text = glLibObjText("Level X",Font_ALGER_100,(255,200,0))
                elif(Level>10):
                    Level=10

                Level_pos=0
                BossPrepare=False
                BossScene=False
                Cubes = []
                for z in range(-110,-10,18-Level):
                    GenerateCube(z)
                        
                
            if event.key == K_z or event.key == K_y or event.key == K_MINUS or event.key == K_KP_MINUS:
                Level-=1
                if(Level>1):
                    Level_Text = glLibObjText("Level "+str(Level),Font_ALGER_100,(255,200,0))
                else:
                    Level=1

                Level_pos=0
                BossPrepare=False
                BossScene=False
                Cubes = []
                for z in range(-110,-10,18-Level):
                    GenerateCube(z)


##            #Wechsle Fulscreen Modus
##            if event.key == K_F11:
##                glLibWindow.toggle_fullscreen(Window)
##                Window.flip()

    if key[K_LALT] and key[K_F4] or key[K_RALT] and key[K_F4]:
        pygame.quit()
        sys.exit()

    if key[K_a]: Player.x+=-0.01*speed
    if key[K_w]: Player.y+=0.01*speed
    if key[K_d]: Player.x+=0.01*speed
    if key[K_s]: Player.y+=-0.01*speed

    if key[K_j]: Player.speed_x+=-0.0003*speed
    if key[K_i]: Player.speed_y+=0.0003*speed
    if key[K_l]: Player.speed_x+=0.0003*speed
    if key[K_k]: Player.speed_y+=-0.0003*speed
    if key[K_o]: Player.speed_z+=0.0003*speed
    if key[K_p]: Player.speed_z+=-0.003*speed

    if key[K_LEFT]: Camera_pos[0]-=1*speed
    if key[K_RIGHT]: Camera_pos[0]+=1*speed
    if key[K_UP]: Camera_pos[2]-=1*speed
    if key[K_DOWN]: Camera_pos[2]+=1*speed
    if key[K_0]: Camera_pos = [0,0.5,6]

    if key[K_TAB]:
        speed*=4
        Tap_Press=True
    else:
        Tap_Press=False

    if key[K_RETURN]:
        speed*=4
        Enter_Press=True
    else:
        Enter_Press=False



    Camera.set_target_pos(Camera_pos)
    Staturbar_Camera.set_target_pos(Camera_pos)

    Player.x+=Player.speed_x*speed
    Player.y+=Player.speed_y*speed
    Player.z+=Player.speed_z*speed

    if(Player.x<-1.5):
        Player.x=-1.5
        Player.speed_x*=-0.25
        #Player.speed_x=abs(Player.speed_x)**2
    if(Player.x>1.5):
        Player.x=1.5
        Player.speed_x*=-0.25
        #Player.speed_x=(Player.speed_x**2)*-1
    if(Player.y<-1.5):
        Player.y=-1.5
        Player.speed_y*=-0.25
    if(Player.y>1.5):
        Player.y=1.5
        Player.speed_y*=-0.25
    if(Player.z<-10):
        Player.z=-10
        Player.speed_z*=-0.25
    if(Player.z>4):
        Player.z=4
        Player.speed_z*=-0.25


    Camera.update()
    Staturbar_Camera.update()

    Window.clear()

    Statusbar.set_view()
    Staturbar_Camera.set_camera()
    Staturbar_Sun.draw()

    #P+=0.001
    #glTranslated(0,-1.5,0)

    #glLibTexturing(True)

    #Level_Text = glLibObjText("Level 1   Leben 7   Zeit: 10:61.345",Font_ALGER_100,(255,128,50))

    if(Leben_alt<>Leben):
        Leben_alt=Leben
        if(Leben<10):
            Lives_Text = glLibObjText("Lives 0"+str(Leben),Font_ALGER_100,(255,30,10))
        else:
            Lives_Text = glLibObjText("Lives "+str(Leben),Font_ALGER_100,(255,30,10))
    if(Enter_Press==False and Tap_Press==False):
        Time=time.clock()-Startzeit-Pause_Time
        if(Time<100):
            if(Time<10):
                Time_Text = glLibObjText("Time "+str(round(Time,2)),Font_ALGER_100,(0,200,200))
            else:
                Time_Text = glLibObjText("Time "+str(round(Time,1)),Font_ALGER_100,(0,200,200))
        else:
            Time_Text = glLibObjText("Time "+str(int(round(Time,0))),Font_ALGER_100,(0,200,200))
    else:
        ZPos=int(round(Level_pos,0))
        if(ZPos<10):
            Time_Text = glLibObjText("ZPos 00"+str(ZPos),Font_ALGER_100,(0,200,255))
        elif(ZPos<100):
            Time_Text = glLibObjText("ZPos 0"+str(ZPos),Font_ALGER_100,(0,200,255))
        else:
            Time_Text = glLibObjText("ZPos "+str(ZPos),Font_ALGER_100,(0,200,255))
        
        
    if(Tap_Press==False):  
        FPS_Text = glLibObjText("FPS "+str(int(round(60/speed,0))),Font_ALGER_100,(128,255,50))
    else:            
        FPS_Text = glLibObjText("FPS "+str(int(round(60/(speed/4),0))),Font_ALGER_100,(255,128,50))
    

    glScalef(4,4,4);
    glTranslated(-7.7,-0.5,0)
    Level_Text.draw()
    glTranslated(4,0,0)
    Lives_Text.draw()
    glTranslated(4.1,0,0)
    Time_Text.draw()
    glTranslated(4.5,0,0)
    FPS_Text.draw()
    glTranslated(-8.4,0.5,0)
    glScalef(0.25,0.25,0.25);

    glLibSelectTexture(Texture_Player)




    View3D.set_view()
    Camera.set_camera()
    Sun.draw()

    #BGround.x=-0.25
    #BGround.y=-0.25
##    BGround.z+=0.01*speed
##    glScalef(10,10,10);
##    glTranslated(BGround.x,BGround.y,BGround.z)
##    BGround.draw()
##    glTranslated(-BGround.x,-BGround.y,-BGround.z)
##    glScalef(0.1,0.1,0.1);


##    glTranslated(-0.5,Player.y,5+Player.x+10)
##    BGround.draw(n)
##    glTranslated(-0.5,-Player.y,-5+Player.x+10)


    Player_Schutzzeit-=1
    GenerateNewArea=0
    Object_ID=-1
    for Cube in Cubes:
        Object_ID+=1
        if(Cube.z>5):
            GenerateNewArea=Cube.z-100
            Cubes.pop(Object_ID)
        if(SphereRectCollision(Player,Cube)==True):
            if(Cube.cube_type==1):
                Leben+=1
            else:
                if(Player_Schutzzeit<0):
                    Player_Schutzzeit=4
                    Leben-=1

                if(Leben==0):
                    print 'Tot!'
                    #pygame.mixer.music.fadeout(1)
                    pygame.mixer.music.load(Sound_GameOver)
                    pygame.mixer.music.play(-1)
                    for Cube in Cubes:
                        Cube.z-=60

                    for i in range(int(round(600/speed))):
                        x=random.uniform(-Cube_speed_z[Level-1],Cube_speed_z[Level-1])
                        y=random.uniform(-Cube_speed_z[Level-1],Cube_speed_z[Level-1])
                        z=random.uniform(-Cube_speed_z[Level-1],Cube_speed_z[Level-1])
                        magnitude  = sqrt(x**2 + y**2 + z**2)
                        Player_Particles.append(glLibObjTexSphere(random.uniform(0.1,0.2),64,Player.x,Player.y,Player.z+0.5,x/magnitude/random.uniform(75,85), y/magnitude/random.uniform(75,85), z/magnitude/random.uniform(75,85),Cube.r,Cube.g,Cube.b,255,0,0,0,2,round(400/speed)))

                print Leben

            #if(Leben>0):
            for i in range(int(round(300/speed))):
                x=random.uniform(-Cube_speed_z[Level-1],Cube_speed_z[Level-1])
                y=random.uniform(-Cube_speed_z[Level-1],Cube_speed_z[Level-1])
                z=random.uniform(-Cube_speed_z[Level-1],Cube_speed_z[Level-1])
                magnitude  = sqrt(x**2 + y**2 + z**2)
                Particles.append(glLibObjCube(random.uniform(0.03,0.09),Player.x,Player.y,Player.z+0.5,x/magnitude/random.uniform(45,55), y/magnitude/random.uniform(45,55), z/magnitude/random.uniform(45,55),Cube.r,Cube.g,Cube.b,Transparence,2,round(300/speed)))
            Cubes.pop(Object_ID)

    if(more_FPS==False):
        #Hier habe ich absichtlich Star_obj.draw() und Stars.pop() in die gleiche for Star in Stars Schleife gemacht da dadurch viele Ressourcen gespart sowie durch das unsaubere Löschen coole Blinkeffekte entstehen.
        Object_ID=-1
        for Star in Stars:
            Object_ID+=1
            if(Star.z>5):
                Stars.pop(Object_ID)
                Stars.append(glLibObjStar(random.uniform(0.01,0.03),random.uniform(-20,20),random.uniform(-20,20),random.uniform(-90,110),0,0,Cube_speed_z[Level-1],random.randint(100,255),random.randint(100,255),random.randint(100,255),Transparence,0))
            Star.x+=Star.speed_x*speed
            Star.y+=Star.speed_y*speed
            Star.z+=Star.speed_z*speed
            glTranslated(Star.x,Star.y-0.8,Star.z+0.8)
            glRotatef(90,1,0,0)
            glScalef(Star.size,Star.size,Star.size);
            glLibColor((Star.x,Star.y,Star.z))
            Star_obj.draw()
            glScalef(1/Star.size,1/Star.size,1/Star.size);
            glRotatef(-90,1,0,0)
            glTranslated(-Star.x,-Star.y+0.8,-Star.z-0.8)


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


    if(Leben==0):
        glLibColor((255,255,255,255))
        glTranslated(-1.3,0.6,2)
        Death_Game.draw()
        glTranslated(0.2,-0.8,0)
        Death_Over.draw()
        glTranslated(1.1,0.2,-2)
        glLibSelectTexture(Texture_Player)

        Object_ID=-1
        for Particle in Player_Particles:
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
                Player_Particles.pop(Object_ID)
        if(Object_ID==-1):
            Leben=7
            Level_pos=0
            pygame.mixer.music.load(Sound[random.randint(0,1)])
            pygame.mixer.music.play(-1)
            Pause_Time=0
            Startzeit=time.clock()
    elif(BossScene==True):


        Object_ID=-1
        glScalef(0.1,0.1,0.1);
        for Particle in BossCube_Particles:
            Object_ID+=1
            Particle.x+=Particle.speed_x*speed
            Particle.y+=Particle.speed_y*speed
            Particle.z+=Particle.speed_z*speed

            Particle.rotate_x+=random.uniform(0,2)*speed
            Particle.rotate_y=random.uniform(0,2)*speed
            Particle.rotate_z+=random.uniform(0,2)*speed
             
            glRotatef(Particle.rotate_x,0,1,0)
            glRotatef(Particle.rotate_y,1,0,0)
            glRotatef(Particle.rotate_z,1,0,0)
            glTranslated(Particle.x,Particle.y,Particle.z)
            Particle.draw()
            glTranslated(-Particle.x,-Particle.y,-Particle.z)
            glRotatef(-Particle.rotate_z,1,0,0)
            glRotatef(-Particle.rotate_y,1,0,0)
            glRotatef(-Particle.rotate_x,0,1,0)
            
            Particle.time-=1
            
##            if(Particle.time==0):
##                BossCube_Particles.pop(Object_ID)
        glScalef(10,10,10);


        if(Object_ID==-1):
            if(SphereRectCollision(Player,BossCube)==True):
                pygame.mixer.music.load(Sound_LevelUp)
                pygame.mixer.music.play(-1)
                Player.a=220
                for i in range(int(round(1500/speed))):
                            x=random.uniform(-Cube_speed_z[Level-1],Cube_speed_z[Level-1])
                            y=random.uniform(-Cube_speed_z[Level-1],Cube_speed_z[Level-1])
                            z=random.uniform(-Cube_speed_z[Level-1],Cube_speed_z[Level-1])
                            magnitude  = sqrt(x**2 + y**2 + z**2)
                            BossCube_Particles.append(glLibObjBossCube(random.uniform(0.1,0.2),BossCube.x,BossCube.y,BossCube.z+1,x/magnitude/random.uniform(45,75), y/magnitude/random.uniform(45,75), z/magnitude/random.uniform(45,55),255,0,0,0,2,round(800/speed)))

            BossCube.x+=BossCube.speed_x*speed
            BossCube.y+=BossCube.speed_y*speed
            BossCube.z+=BossCube.speed_z*speed

            BossCube.rotate_x+=1*speed
            BossCube.rotate_y=1*speed
            BossCube.rotate_z+=1*speed

            glTranslated(BossCube.x,BossCube.y,BossCube.z)
            glRotatef(BossCube.rotate_x,0,1,0)
            glRotatef(BossCube.rotate_y,1,0,0)
            glRotatef(BossCube.rotate_z,1,0,0)
            glScalef(6,6,6);
            BossCube.draw()
            glScalef(0.166666667,0.166666667,0.166666667);
            glRotatef(-BossCube.rotate_z,1,0,0)
            glRotatef(-BossCube.rotate_y,1,0,0)
            glRotatef(-BossCube.rotate_x,0,1,0)
            glTranslated(-BossCube.x,-BossCube.y,-BossCube.z)

        else:
            if(BossCube_Particles[0].time<300):
                glLibColor((255,255,255,255))
                glTranslated(-1.3,0.6,2)
                BossCube_Level.draw()
                glTranslated(0.76,-0.8,0)
                BossCube_Up.draw()
                glTranslated(0.54,0.2,-2)
                glLibSelectTexture(Texture_Player)

                if(BossCube_Particles[0].time<50):
                    BossCube_Particles = []
##                    Prticles_count=BossCube_Particles.__len__()
##                    for i in range(Prticles_count):
##                        BossCube_Particles.pop()
                    BossCube.z=-100
                    Player.a=255
                    Level+=1
                    if(Level<10):
                        Level_Text = glLibObjText("Level "+str(Level),Font_ALGER_100,(255,200,0))
                    elif(Level==10):
                        Level_Text = glLibObjText("Level X",Font_ALGER_100,(255,200,0))
                    elif(Level<1):
                        Level=1
                    else:
                        #End Screen
                        pygame.mixer.music.load(Sound[2])
                        pygame.mixer.music.play(-1)
                        
                        Level=10
                        View3D = glLibView3D((0,0,Screen[0],Screen[1]),45)
                        Window.clear()

                        View3D.set_view()
                        Camera.set_camera()
                        Sun.draw()

                        End_Text_1 = glLibObjText("Congratulations",Font_ALGER_100,(255,200,0))
                        End_Text_2 = glLibObjText("You've reached the",Font_ALGER_100,(255,200,0))
                        End_Text_3 = glLibObjText("end of the game",Font_ALGER_100,(255,200,0))
                        End_Text_4 = glLibObjText("Hopefully you had fun",Font_ALGER_100,(255,200,0))
                        End_Text_5 = glLibObjText("and will play it again",Font_ALGER_100,(255,200,0))
                        End_Text_6 = glLibObjText("Enjoy yourself!",Font_ALGER_100,(255,200,0))
                        End_Text_7 = glLibObjText("Nico Bosshard",Font_ALGER_100,(255,200,0))
                        glDisable(GL_DEPTH_TEST)
                        glLibColor((255,255,255,255))
                        glScalef(0.5,0.5,0.5)

                        z=-40
                        glTranslated(0,0,-40)
                        while z<10:
                            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                            glTranslated(-3.6,3,0.03*speed)
                            z+=0.03*speed
                            End_Text_1.draw()
                            glTranslated(-0.4,-0.9,0)
                            End_Text_2.draw()
                            glTranslated(0.8,-0.9,0)
                            End_Text_3.draw()
                            glTranslated(-1.46,-1.2,0)
                            End_Text_4.draw()
                            glTranslated(0.05,-0.9,0)
                            End_Text_5.draw()
                            glTranslated(1.45,-1.2,0)
                            End_Text_6.draw()
                            glTranslated(0.4,-0.9,0)
                            End_Text_7.draw()
                            #-3.6-0.4+0.8-1.46+0.05+1.45+0.4=-2.76 => 2.76
                            #3-0.9-0.9-1.2-0.9-1.2-0.9=-3 => 3
                            glTranslated(2.76,3,0)
                            
                            frame_time=time.clock()
                            speed=(frame_time-frame_time_alt)*60
                            frame_time_alt=frame_time
                            
                            Window.flip()
                            #time.sleep(0.05)


                        #glTranslated(0,0,-100)
                        glScalef(2,2,2)
                        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                        Window.flip()
                        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                        End_Text_8 = glLibObjText("The",Font_ALGER_100,(255,200,0))
                        End_Text_9 = glLibObjText("End",Font_ALGER_100,(255,200,0))
                        glScalef(2,2,2)
                        while z>-20:
                            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                            glTranslated(-0.75,0.1,-0.03*speed)
                            z-=0.03*speed
                            End_Text_8.draw()
                            glTranslated(0.08,-0.8,0)
                            End_Text_9.draw()
                            glTranslated(0.67,0.7,0)

                            frame_time=time.clock()
                            speed=(frame_time-frame_time_alt)*60
                            frame_time_alt=frame_time

                            Window.flip()

                        glTranslated(0,0,20)
                        glScalef(0.5,0.5,0.5)

                        glLibTexturing(False)
                        glLibColor((255,255,255,255))

                        speed=6
                        for i in range(int(round(1500/speed))):
                            x=random.uniform(-Cube_speed_z[Level-1],Cube_speed_z[Level-1])
                            y=random.uniform(-Cube_speed_z[Level-1],Cube_speed_z[Level-1])
                            z=random.uniform(-Cube_speed_z[Level-1],Cube_speed_z[Level-1])
                            magnitude  = sqrt(x**2 + y**2 + z**2)
                            BossCube_Particles.append(glLibObjBossCube(random.uniform(0.1,0.2),0,0,0,x/magnitude/random.uniform(145,175), y/magnitude/random.uniform(145,175), z/magnitude/random.uniform(145,155),255,0,0,0,2,round(9000/speed)))

                        #glScalef(0.1,0.1,0.1);
                        while (BossCube_Particles[0].time>50):
                            #glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                            Object_ID=-1
                            for Particle in BossCube_Particles:
                                Object_ID+=1
                                Particle.x+=Particle.speed_x*speed
                                Particle.y+=Particle.speed_y*speed
                                Particle.z+=Particle.speed_z*speed

                                Particle.rotate_x+=random.uniform(0,2)*speed
                                Particle.rotate_y=random.uniform(0,2)*speed
                                Particle.rotate_z+=random.uniform(0,2)*speed
                                 
                                glRotatef(Particle.rotate_x,0,1,0)
                                glRotatef(Particle.rotate_y,1,0,0)
                                glRotatef(Particle.rotate_z,1,0,0)
                                glTranslated(Particle.x,Particle.y,Particle.z)
                                Particle.draw()
                                glTranslated(-Particle.x,-Particle.y,-Particle.z)
                                glRotatef(-Particle.rotate_z,1,0,0)
                                glRotatef(-Particle.rotate_y,1,0,0)
                                glRotatef(-Particle.rotate_x,0,1,0)
                                
                                Particle.time-=1
                            Window.flip()


                        #glScalef(10,10,10);
                        glEnable(GL_DEPTH_TEST)

                        pygame.quit()
                        sys.exit()
                    Level_pos=0
                    BossPrepare=False
                    BossScene=False
                    for z in range(-110,-10,18-Level):
                        GenerateCube(z)
                    pygame.mixer.music.load(Sound[random.randint(0,2)])
                    pygame.mixer.music.play(-1)




    else:
        for Cube in Cubes:
            Cube.x+=Cube.speed_x*speed
            Cube.y+=Cube.speed_y*speed
            Cube.z+=Cube.speed_z*speed
            if(Cube.cube_type==1): #Herz
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


        #glTranslated(-Player.x,-Player.y,-Player.z)
        #glRotatef(-10,Player.x,Player.y,Player.z)

        Level_pos+=Cube.speed_z*speed
        #print Level_pos

        if(Level_pos>Level_length-110):
            if(Level_pos>Level_length):
                BossScene=True
            else:
                BossPrepare=True

    if(Leben>0):
        glLibColor((Player.r,Player.g,Player.b,Player.a))
        glTranslated(Player.x,Player.y,Player.z)
        #r+=sqrt(Player.speed_x**2 + Player.speed_y**2 + Player.speed_z**2)*100
        Player.rotate_x+=Player.speed_x*100*speed
        Player.rotate_y+=Player.speed_y*100*speed
        Player.rotate_z+=Player.speed_z*100*speed
        #if not (Player.speed_x==0 and Player.speed_y==0 and Player.speed_z==0):
        glRotatef(Player.rotate_x,0,1,0)
        glRotatef(-Player.rotate_y,1,0,0)
        glRotatef(Player.rotate_z,1,0,0)
        #print Player.speed_x*10000
        Player.draw()
        glRotatef(-Player.rotate_z,1,0,0)
        glRotatef(Player.rotate_y,1,0,0)
        glRotatef(-Player.rotate_x,0,1,0)



        glTranslated(-Player.x,-Player.y,-Player.z)


    frame_time=time.clock()
    speed=(frame_time-frame_time_alt)*60
    #print speed
    frame_time_alt=frame_time

    Window.flip()

    if(BossPrepare==False):
        GenerateNewArea_Schutzzeit-=1
        if(GenerateNewArea<0 and GenerateNewArea_Schutzzeit<1):
            GenerateNewArea_Schutzzeit=3
            GenerateCube(GenerateNewArea)

