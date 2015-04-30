"""
 A simple Game nemed Flootmoion
 Developed by NicoBosshard <nico@bosshome.ch>

 http://www.nicobosshard.ch

Known Bugs:
- Nothing -

To-Do:
- Kollisions Sounds suchen
- BossCube als Icon
- Comments in Surce Code verbessern
- Start screen picture
- Sphere Textur
    - Löscher unützen Texturen
- F1 Hilfe verbessern
- GitHub Repository
"""
import Leap, sys, threading, math, pygame, random, time, webbrowser #Some usual Libary staff.
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture #Leap Motion a movment control system
from pygame.locals import * #pygame is a Game Engine like SDL2 for Python but probably bether then pySDL2
from OpenGL.GL import * #OpenGL the best grafic libary ever!
from OpenGL.GLU import * #And other pyOpenGL staff
from OpenGLLibrary import * #A GameEnigine that I have downloaded and modivied I also add some Functions to it and fixed bugs.
import main #To get the main.pyc file.

#Set the background soundpPaths
Sound=["./sound/Sound1.mp3","./sound/Sound2.mp3","./sound/Sound3.mp3"]
Sound_GameOver="./sound/GameOver.mp3"
Sound_LevelUp="./sound/LevelUp.mp3"

#Play a random backgrund sound
pygame.mixer.init(size=-16, channels=2, buffer=4096)
pygame.mixer.music.load(Sound[random.randint(0,2)]) #random.randint(1,2)
pygame.mixer.music.play(-1)

#Load sound effects - mp3 dosn't work with pygame.mixer.Sound!
boom = [pygame.mixer.Sound("./sound/boom.wav"),pygame.mixer.Sound("./sound/boom.wav"),pygame.mixer.Sound("./sound/boom.wav")]
GetLive = pygame.mixer.Sound("./sound/boom.wav")
baem = pygame.mixer.Sound("./sound/boom.wav")


#Set the defult Values to be indebendent from a defect config.ini File
Camera_pos = [0,0.5,6]

Version="Floatmotion 1.0"
PublishDate="20.04.2015"
Programmer="Nico Bosshard"
EMail="nico@bosshome.ch"
Level=1
Leben_Respawnvalue=7
Leben=7
Player_Schutzzeit=0
Zeit=0
Startzeit=0

Leben_alt=0

Level_pos=0
Level_length=500
BossPrepare=False
BossScene=False

LeapConected=False
MouseNoKlick=True
EndlessMode=False
EndlessMode_ShowText=0
FastForward=1.0
BackslashL_Active=False
Backquote_Active=False
Shift_Active=False
TurnStatusbar=False
more_FPS=False

Screen_with=1280
Screen_high=720
Fulscreen=False
Screenshotpath=".\\"
INSTDIR=".\\"
PROFILE=".\\"
DOCUMENTS=".\\"
PICTURES=".\\"
DESKTOP=".\\"

#Ich habe sogar den ini reader selbst programmirt!
#Ih habe absichtlich kein # implementiert da es sonst probleme geben würde wenn der Pfad ein # enhalten würde.
with open("config.ini") as f:
    for line in f:
        line=line.replace('\n', "") 
        words=line.split('=')
        
        if(words.__len__()==2):
            if(section=="[Info]"):
                if(words[0]=="Version"):
                    Version=words[1]
                if(words[0]=="PublishDate"):
                    PublishDate=words[1]
                if(words[0]=="Programmer"):
                    Programmer=words[1]
                if(words[0]=="E-Mail"):
                    EMail=words[1]
            
            if(section=="[Path]"):
                if(words[0]=="INSTDIR"):
                    INSTDIR=words[1]
                if(words[0]=="PROFILE"):
                    PROFILE=words[1]
                if(words[0]=="DOCUMENTS"):
                    DOCUMENTS=words[1]
                if(words[0]=="PICTURES"):
                    PICTURES=words[1]
                if(words[0]=="DESKTOP"):
                    DESKTOP=words[1]
                            
            if(section=="[Graphics]"):
                if(words[0]=="Screen_with"):
                    Screen_with=eval(words[1])
                if(words[0]=="Screen_high"):
                    Screen_high=eval(words[1])

                if(words[0]=="Fullscreen"):
                    if(words[1]=="true"): #Erst wird true geprüft da defult
                        Fulscreen=True
                    elif(words[1]=="false"):
                        Fulscreen=False
                    else:
                        print "Error in config.ini File Line:",line,"Fullscreen can only be true or false. To not interrupt the programmstart it was automaticly set to true."
                        Fulscreen=True

                if(words[0]=="noStars(more_FPS)"):
                    if(words[1]=="false"): #Erst wird false geprüft da defult
                        more_FPS=False
                    elif(words[1]=="true"):
                        more_FPS=True
                    else:
                        print "Error in config.ini File Line:",line,"noStars(more_FPS) can only be true or false. To not interrupt the programmstart it was automaticly set to false."
                        more_FPS=False

            if(section=="[Scoreboard]" and words[0]=="TurnStatusbar"):
                if(words[1]=="false"): #Erst wird false geprüft da defult
                    TurnStatusbar=False
                elif(words[1]=="true"):
                    TurnStatusbar=True
                else:
                    print "Error in config.ini File Line:",line,"TurnStatusbar can only be true or false. To not interrupt the programmstart it was automaticly set to false."
                    TurnStatusbar=False

            if(section=="[Control]" and words[0]=="MouseNoKlick(mouse Only)"):
                if(words[1]=="true"): #Erst wird true geprüft da defult
                    MouseNoKlick=True
                elif(words[1]=="false"):
                    MouseNoKlick=False
                else:
                    print "Error in config.ini File Line:",line,"MouseNoKlick can only be true or false. To not interrupt the programmstart it was automaticly set to true."
                    MouseNoKlick=True

            if(section=="[Default]"):
                if(words[0]=="EndlessMode"):
                    if(words[1]=="false"): #Erst wird false geprüft da defult
                        EndlessMode=False
                    elif(words[1]=="true"):
                        EndlessMode=True
                    else:
                        print "Error in config.ini File Line:",line,"EndlessMode can only be true or false. To not interrupt the programmstart it was automaticly set to false."
                        EndlessMode=False

                if(words[0]=="FastForward"):
                    FastForward=eval(words[1])
                
                if(words[0]=="Level"):
                    Level=eval(words[1])

                if(words[0]=="Lives"):
                    Leben=eval(words[1])
                    Leben_Respawnvalue=eval(words[1])

                if(words[0]=="Level_length"):
                    Level_length=eval(words[1])

            if(section=="[Camera]"):
                if(words[0]=="Camera_pos.x"):
                    Camera_pos[0]=eval(words[1])

                if(words[0]=="Camera_pos.y"):
                    Camera_pos[1]=eval(words[1])

                if(words[0]=="Camera_pos.z"):
                    Camera_pos[2]=eval(words[1])
            
            print line.split('=')
        else:
            section=line


#A Function to generate a 3x3 feld Cubes. It's maybe the hart of my program.
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

    #If all 9 cubes are generated there will be no possibility to don't lose a live so the next lines replaces all 9 Cubes with heart cubes.
    if(Cubes_count==9):
        for i in range(9):
            Cubes.pop() #by Defult remove last Objekt
        Cubes_count-=9
        for x in range(-1,2):
            for y in range(-1,2):
                Cubes.append(glLibObjCube(0.5,x,y,z,0,0,Cube_speed_z[Level-1],255,0,0,100,1))
        Hearts_count+=9


##def LevelReload():
##    Level_pos=0
##    BossPrepare=False
##    BossScene=False
##    Cubes = []
##    for z in range(-110,-10,18-Level):
##        GenerateCube(z)

#If the programm don't reponse to any Events windows make the Window white and means that the program crashed. Also It's always usefull if the exit keys works.
def EndCutscene_key():
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE or key[K_LALT] and key[K_F4] or key[K_RALT] and key[K_F4]:
                pygame.quit()
                sys.exit()

#A Function th check if a sphere colise with a cube. To uderstand how it works you have to imagen what it do and maybe also draw it through a paper.
def SphereRectCollision(sphere, rect):
    sphereXDistance = abs(sphere.x - rect.x)
    sphereYDistance = abs(sphere.y - rect.y)
    sphereZDistance = abs(sphere.z - rect.z)

    if(sphereXDistance >= (rect.size + sphere.radius)): return False
    if(sphereYDistance >= (rect.size + sphere.radius)): return False
    if(sphereZDistance >= (rect.size + sphere.radius)): return False

    if(sphereXDistance < (rect.size)): return True
    if(sphereYDistance < (rect.size)): return True
    if(sphereZDistance < (rect.size)): return True

    cornerDistance_sq = (sphereXDistance - rect.size)**2 + (sphereYDistance - rect.size)**2 + (sphereYDistance - rect.size)**2

    return (cornerDistance_sq < (sphere.radius * sphere.radius))


#The whole LeapMotion Listener.
class LeapMotionListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        main.LeapConected=True
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        main.LeapConected=False
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

        main.LeapConected=True

##            print Player.speed_x
##            print Player.speed_y
##            print Player.speed_z



#Creat and start the LeapMotion Listener
listener = LeapMotionListener()
controller = Leap.Controller()
controller.add_listener(listener)
frame = controller.frame()


#Initialize the display module, hide the mouse and set the title image
pygame.init()
pygame.mouse.set_visible(False)
System_Icon = pygame.image.load("img/Cube.ico")
pygame.display.set_icon(System_Icon)
screen = pygame.display.set_mode((Screen_with, Screen_high))
Titleimage = pygame.image.load("img/Leap.jpg")
imagerect = Titleimage.get_rect()
screen.blit(pygame.transform.scale(Titleimage, (Screen_with, Screen_high)), (0, 0))
pygame.display.flip()

#Preparing some Variables for the later user. The diffrence between the global variables on the top of thepProgramm is that ths have to to with grafic or FPS
speed=1
frame_time=time.clock()
frame_time_alt=time.clock()

random.seed(time.clock())
Screen = (Screen_with,Screen_high)
Cube_speed_z=[0.05,0.055,0.06,0.065,0.07,0.075,0.08,0.085,0.09,0.1]
Transparence=200
r=0
GenerateNewArea_Schutzzeit=0
Window = glLibWindow(Screen,Fulscreen,System_Icon,"Float Motion - Nico Bosshard",False)
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

#Load the Font ALGER.TTF
Font_ALGER_100 = pygame.font.Font(os.path.join("Fonts","ALGER.TTF"),100)

#Generate some Texts.
Pause_Text = glLibObjText("Pause",Font_ALGER_100,(255,255,0))
Pause_Ready = glLibObjText("Ready",Font_ALGER_100,(255,200,0))
Pause_GO = glLibObjText("GO",Font_ALGER_100,(0,255,0))

Death_Game = glLibObjText("Game",Font_ALGER_100,(200,250,70))
Death_Over = glLibObjText("Over",Font_ALGER_100,(255,220,60))

BossCube_Level = glLibObjText("Level",Font_ALGER_100,(255,200,0))
#BossCube_Up = glLibObjText("Up",Font_ALGER_100,(180,230,30))
BossCube_Up = glLibObjText("Up",Font_ALGER_100,(255,230,30))

EndlessMode_Endless=glLibObjText("Endless",Font_ALGER_100,(64,128,255))
EndlessMode_Normal=glLibObjText("Normal",Font_ALGER_100,(64,255,64))
EndlessMode_Mode=glLibObjText("Mode",Font_ALGER_100,(255,200,0))

Level_Text = glLibObjText("Level "+str(Level),Font_ALGER_100,(235,255,0))
Lives_Text = glLibObjText("Lives "+str(Leben),Font_ALGER_100,(255,30,10))

#Create Objects and Load *.obj and Textures for the later use.
Player = glLibObjTexSphere(0.3,64,0,0,2)
Player_Particles = []
#Texture_Player = glLibTexture("textures/Oak Ligh.bmp"
Texture_Player = glLibTexture("textures/Limeston.bmp")
Statusbar_hearts = []
Cubes = []
Particles = []
Stars = []
BossCube=glLibObjBossCube(3,0,0,-100,0,0,0.1,255,0,0,0,0,-1)
BossCube_Particles = []

#BGround = glLibObjFromFile("obj/leer.obj")
Star_obj = glLibObjFromFile("obj/Star.obj")
Heart_obj = glLibObjFromFile("obj/Heart.obj")


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


#And the ast thin before the main Loop
#glClearColor( 1, 1, 1, 1)
glLibTexturing(True)
glEnable(GL_DEPTH_TEST)
#glDisable(GL_DEPTH_TEST)


Pause_Startzeit=0
Pause_Time=0
Startzeit=time.clock()


#Begin of the main Loop
while True:

    #Muse Controller Funcion
    MousePressed=pygame.mouse.get_pressed()
    if(MouseNoKlick==True or MousePressed[0]==True or MousePressed[1]==True or MousePressed[2]==True and LeapConected==False):
        MousePos=pygame.mouse.get_pos()
        Player.speed_x=((MousePos[0]-(Screen_with/2))/16-Player.x)/(200*speed)
        Player.speed_y=-((MousePos[1]-(Screen_high/2))/16-Player.y)/(200*speed)


    #Everithing for you can use the keyboard comes in then next lines
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if(event.type == MOUSEBUTTONUP and MouseNoKlick==False):
            Player.speed_x=0
            Player.speed_y=0
            Player.speed_z=0

        #The next Functions neads only one call when a key get pressed.
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE or key[K_LALT] and key[K_F4] or key[K_RALT] and key[K_F4]:
                pygame.quit()
                sys.exit()

            #print event.key

            #Hilfe Funktion
            if event.key == K_F1 or event.key == K_HELP:
                webbrowser.open("Help.mht")


            #Toggle MouseNoKlick
            if event.key == K_q:
                if(MouseNoKlick==False):
                    MouseNoKlick=True
                else:
                    MouseNoKlick=False
                    Player.speed_x=0
                    Player.speed_y=0
                    Player.speed_z=0


            #Pause Funktionn
            if event.key == K_PAUSE or event.key == K_SPACE or event.key == K_F1 or event.key == K_HELP:
                Pause_Startzeit=time.clock()

                #Der depth test wird temporär ausgeshaltet, dammit keine Würfel vor der Schrift gezeichnet werden können.
                glDisable(GL_DEPTH_TEST)
                glTranslated(-1.4,0.8,2)
                Pause_Text.draw()
                Window.flip()

                Flip_1or2=1

                no_continue_key_press=True
                while no_continue_key_press:
                    time.sleep(0.5)
                    for event_p in pygame.event.get():
                        if(event_p.type == KEYDOWN):
                            if event_p.key == K_F1 or event.key == K_HELP:
                                webbrowser.open("Help.mht")
                            else:
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

            
            if(event.key == K_EQUALS):
                FastForward=1.0

            if event.key == K_RIGHTBRACKET:
                if(FastForward>=9):
                    FastForward+=1
                elif(FastForward>=5):
                    FastForward+=0.5
                elif(FastForward>=2):
                    FastForward+=0.2
                else:
                    FastForward+=0.1

            if event.key == K_BACKSLASH:
                if(FastForward>=9):
                    FastForward-=1
                elif(FastForward>=5):
                    FastForward-=0.5
                elif(FastForward>=2):
                    FastForward-=0.2
                else:
                    FastForward-=0.1


            #SlowForward 0.5x
            if event.key == 60 : #Key links von Shift
                if(BackslashL_Active==False):
                    BackslashL_Active=True
                    FastForward*=0.5
                else:
                   BackslashL_Active=False
                   FastForward*=2

            #FastForward 2x
            if event.key == K_BACKQUOTE :
                if(Backquote_Active==False):
                    Backquote_Active=True
                    FastForward*=2
                else:
                   Backquote_Active=False
                   FastForward*=0.5

            #FastForward 4x
            if event.key == K_LSHIFT or event.key == K_RSHIFT :
                if(Shift_Active==False):
                    Shift_Active=True
                    FastForward*=4
                else:
                    Shift_Active=False
                    FastForward*=0.25


            if event.key == K_RETURN:
                if(TurnStatusbar==False):
                    TurnStatusbar=True
                else:
                    TurnStatusbar=False

            #More FPS Funkttion (no Stars)
            if event.key == K_F2:
                if(more_FPS==False):
                    more_FPS=True
                else:
                    more_FPS=False

            #Screenshotspeicherungsfunktion
            if event.key == K_F5:
                while True:
                    print Screenshotpath+time.strftime("%a, %d %b %Y %H-%M-%S", time.gmtime())+".png"
                    try:pygame.image.load(Screenshotpath+time.strftime("%a, %d %b %Y %H-%M-%S", time.gmtime())+".png")
                    except:glLibSaveScreenshot(Screenshotpath+time.strftime("%a, %d %b %Y %H-%M-%S", time.gmtime())+".png");break
                    counter = 1
                    while True:
                        try:pygame.image.load(Screenshotpath+time.strftime("%a, %d %b %Y %H-%M-%S", time.gmtime())+" ("+str(counter)+").png")
                        except:glLibSaveScreenshot(Screenshotpath+time.strftime("%a, %d %b %Y %H-%M-%S", time.gmtime())+" ("+str(counter)+").png");break
                        counter += 1
                    break #Warscheinlich nutzlos aber für die Zukunft.


            #Sehr schöne Platz- und Ressourcensparende Lösung ohne zusätzliche Funktion :D
            if event.key == K_x or event.key == K_PLUS or event.key == K_KP_PLUS or event.key == K_z or event.key == K_y or event.key == K_MINUS or event.key == K_KP_MINUS or event.key >= K_0 and event.key <= K_9:
                if(event.key >= K_0 and event.key <= K_9):
                    Level=event.key-K_0
                    if(Level==0):
                        Level=10
                elif event.key == K_x or event.key == K_PLUS or event.key == K_KP_PLUS:
                    Level+=1
                else: #elif event.key == K_z or event.key == K_y or event.key == K_MINUS or event.key == K_KP_MINUS:
                    Level-=1
                if(Level==1):
                    Level_Text = glLibObjText("Level 1",Font_ALGER_100,(235,255,0))
                if(Level<10 and Level>1):
                    Level_Text = glLibObjText("Level "+str(Level),Font_ALGER_100,(255,255-((Level-1)*20),Level*5))
                elif(Level==10):
                    Level_Text = glLibObjText("Level X",Font_ALGER_100,(255,0,128))
                elif(Level>10):
                    Level=10
                else: #elif Level<1
                   Level=1

                Level_pos=0
                BossPrepare=False
                BossScene=False
                Cubes = []
                for z in range(-110,-10,18-Level):
                    GenerateCube(z)

            #Endless Mode
            if event.key == K_e:
                if(EndlessMode==False):
                    EndlessMode=True
                    EndlessMode_ShowText=25*speed*((more_FPS*1.75)+1)
                else:
                    EndlessMode=False
                    EndlessMode_ShowText=25*speed*((more_FPS*1.75)+1)
                    Level_pos=0
                    BossPrepare=False
                    BossScene=False
                    Cubes = []
                    for z in range(-110,-10,18-Level):
                        GenerateCube(z)
            

            if event.key == K_c:
                Leben=1
            elif event.key == K_v:
                Leben=3
            elif event.key == K_b:
                Leben=7
            elif event.key == K_n:
                Leben-=1
            elif event.key == K_m:
                Leben+=1
            elif event.key == K_COMMA:
                Leben=99


##            #Wechsle Fulscreen Modus - Doesn't work betwenn grafik bugs! Please use the config.ini file for this.
##            if event.key == K_F11:
##                glLibWindow.toggle_fullscreen(Window)
##                Window.flip()


    #Keboard Player Controller
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

    #It's also possibe to move the camera.
    if key[K_LEFT]: Camera_pos[0]-=1*speed
    if key[K_RIGHT]: Camera_pos[0]+=1*speed
    if key[K_UP]: Camera_pos[2]-=1*speed
    if key[K_DOWN]: Camera_pos[2]+=1*speed
    if key[K_LEFTBRACKET]: Camera_pos[1]=1*speed
    if key[39]: Camera_pos[1]-=1*speed

    if key[K_LCTRL] or key[K_RCTRL] or key[K_BACKSPACE]: Camera_pos = [0,0.5,6]


    #Fast Forward 4x as log as Tap is pressed.
    if key[K_TAB]:
        Tap_Press=True
    else:
        Tap_Press=False


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


    #And now the Key thing is finisch and next comes the grafik rendering.
    #First the Window get cleared with black and the view get set to Statusbar
    Camera.update()
    Staturbar_Camera.update()

    Window.clear()

    Statusbar.set_view()
    Staturbar_Camera.set_camera()
    Staturbar_Sun.draw()


    #If the Live value get changed then rerender the Lives Text.
    if(Leben_alt<>Leben):
        Leben_alt=Leben
        if(Leben<0): Leben=0
        if(Leben>99): Leben=99
        if(Leben<10):
            Lives_Text = glLibObjText("Lives 0"+str(Leben),Font_ALGER_100,(255,30,10))
        else:
            Lives_Text = glLibObjText("Lives "+str(Leben),Font_ALGER_100,(255,30,10))

    #The Time since the lasy death or the ZPos neads every frame a rerendering. Which got rerenderd depends if the Statusbar is Toggeld.
    if(TurnStatusbar==False):
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


    #The next lines checks and calculate the FastForward thing
    if(FastForward>16):
        FastForward=16

    if(Tap_Press==False):
        FastForward_Speed=FastForward
    else:
        FastForward_Speed=FastForward*4

    speed*=FastForward_Speed

    
    #And here the FPS or the FastForward value get rerendered every Frame. On normal speed FPS and outherwise the Statusbar shows the FastForward value.
    if(FastForward==1.0 and Tap_Press==False):
        FPS_Text = glLibObjText("FPS "+str(int(round(60/speed,0))),Font_ALGER_100,(128,255,50))
    elif(FastForward_Speed==1):
        FPS_Text = glLibObjText("FF 4",Font_ALGER_100,(255,128,50))
    elif(FastForward_Speed<1):
        FPS_Text = glLibObjText("FF "+str(round(FastForward_Speed,1)),Font_ALGER_100,(128,128,255))
    elif(FastForward_Speed>=10):
        FPS_Text = glLibObjText("FF "+str(int(round(FastForward_Speed,0))),Font_ALGER_100,(((FastForward*8)+127),100*(Tap_Press+1),(FastForward*8)))
    else:
        FPS_Text = glLibObjText("FF "+str(round(FastForward_Speed,1)),Font_ALGER_100,(((FastForward*8)+127),100*(Tap_Press+1),(FastForward*8)))


    #And finaly the rendered Text get drawn throught the screen.
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



    #Now We need also thö render The Game Window so change the view to View3D
    View3D.set_view()
    Camera.set_camera()
    Sun.draw()

##    #Yes my programm used to have a 3D background but I thougt it's nicer to play in the space. So I comit out this Function. Maybe somebody will use it.
##    #BGround.x=-0.25
##    #BGround.y=-0.25
##    BGround.z+=0.01*speed
##    glScalef(10,10,10);
##    glTranslated(BGround.x,BGround.y,BGround.z)
##    BGround.draw()
##    glTranslated(-BGround.x,-BGround.y,-BGround.z)
##    glScalef(0.1,0.1,0.1);

##    glTranslated(-0.5,Player.y,5+Player.x+10)
##    BGround.draw(n)
##    glTranslated(-0.5,-Player.y,-5+Player.x+10)



    #The next staff are the whole OpenGL drawing, moveing and calculating thing. It's a bit compley but you'll understand a lot of it. I't isn't possibly to commit this a lot because you need to understand it or if not then you need to train your imagen.
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
                GetLive.play()
                Leben+=1
            else:
                if(Player_Schutzzeit<0):
                    Player_Schutzzeit=4
                    boom[random.randint(0,2)].play()
                    Leben-=1
                    
                #If ives=0 then preparing the game Over Screen
                if(Leben==0):
                    print 'Tot!'

                    #Change the sound to the Game Over sound
                    #pygame.mixer.music.fadeout(1)
                    pygame.mixer.music.load(Sound_GameOver)
                    pygame.mixer.music.play(-1)

                    #Move all cubes away from the scene
                    for Cube in Cubes:
                        Cube.z-=40

                    #Generate the Player_Particles for the game Over scene. They will be drawn in the main loop
                    for i in range(int(round(400/(speed*(more_FPS+1))))):
                        x=random.uniform(-Cube_speed_z[Level-1],Cube_speed_z[Level-1])
                        y=random.uniform(-Cube_speed_z[Level-1],Cube_speed_z[Level-1])
                        z=random.uniform(-Cube_speed_z[Level-1],Cube_speed_z[Level-1])
                        magnitude  = sqrt(x**2 + y**2 + z**2)
                        Player_Particles.append(glLibObjTexSphere(random.uniform(0.1,0.2),64,Player.x,Player.y,Player.z+0.5,x/magnitude/random.uniform(75,85), y/magnitude/random.uniform(75,85), z/magnitude/random.uniform(75,85),Cube.r,Cube.g,Cube.b,255,0,0,0,2,round(300/(speed*(more_FPS+1)))))

            #Write the amount of Lifes into the Python console.
            print "Leben: ",Leben

            #Generate the Particles that you can see if you hit a cube.
            #if(Leben>0): #Yes I decided that you always se Particles during the Game Over scene. A reason not to show Particles is to have a liddle bit more FPS in the Game Over Scene.
            for i in range(int(round(600/speed))):
                x=random.uniform(-Cube_speed_z[Level-1],Cube_speed_z[Level-1])
                y=random.uniform(-Cube_speed_z[Level-1],Cube_speed_z[Level-1])
                z=random.uniform(-Cube_speed_z[Level-1],Cube_speed_z[Level-1])
                magnitude  = sqrt(x**2 + y**2 + z**2)
                Particles.append(glLibObjCube(random.uniform(0.03,0.09),Player.x,Player.y,Player.z+0.5,x/magnitude/random.uniform(45,55), y/magnitude/random.uniform(45,55), z/magnitude/random.uniform(45,55),Cube.r,Cube.g,Cube.b,Transparence,2,round(300/speed)))
            Cubes.pop(Object_ID) #Remove The cube the Player hit

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


    #Drawing Particles
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


    #Showing Text by changing between Normal- and Endless Mode.
    if(EndlessMode_ShowText>0):
        EndlessMode_ShowText-=1
        glLibColor((255,255,255,255))
        if(EndlessMode==True):
            glTranslated(-1.8,0.3,2)
            EndlessMode_Endless.draw()
            glTranslated(0.65,-0.8,0)
        else:
            glTranslated(-1.75,0.3,2)
            EndlessMode_Normal.draw()
            glTranslated(0.6,-0.8,0)

        #-1.8+0.65=-1.75+0.6=-1.15 => gleiche Rücktranslation
        EndlessMode_Mode.draw()
        glTranslated(1.15,0.5,-2)
        glLibSelectTexture(Texture_Player)


    if(Leben==0):
        glLibColor((255,255,255,255))
        glTranslated(-1.3,0.6,2)
        Death_Game.draw()
        glTranslated(0.2,-0.8,0)
        Death_Over.draw()
        glTranslated(1.1,0.2,-2)
        glLibSelectTexture(Texture_Player)

        #Showing Player Particle so this pard renders the Game Over screen
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

        #The folowing block get executet only once after the Game Over Scene. It reset the Level and Live value.
        if(Object_ID==-1):
            Leben=Leben_Respawnvalue
            Level_pos=0
            pygame.mixer.music.load(Sound[random.randint(0,2)])
            pygame.mixer.music.play(-1)
            Pause_Time=0
            Startzeit=time.clock()

    #Drawing the Level Up Scene
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

            #If the player hit the BossCube then prepaireing the LevelUp scene
            if(SphereRectCollision(Player,BossCube)==True):
                baem.play()
                pygame.mixer.music.load(Sound_LevelUp)
                pygame.mixer.music.play(-1)
                Player.a=220
                for i in range(int(round(1200/(speed*((more_FPS*2)+1))))):
                            x=random.uniform(-Cube_speed_z[Level-1],Cube_speed_z[Level-1])
                            y=random.uniform(-Cube_speed_z[Level-1],Cube_speed_z[Level-1])
                            z=random.uniform(-Cube_speed_z[Level-1],Cube_speed_z[Level-1])
                            magnitude  = sqrt(x**2 + y**2 + z**2)
                            BossCube_Particles.append(glLibObjBossCube(random.uniform(0.1,0.2),BossCube.x,BossCube.y,BossCube.z+1,x/magnitude/random.uniform(45,75), y/magnitude/random.uniform(45,75), z/magnitude/random.uniform(45,55),255,0,0,0,2,600/(speed*((more_FPS*2.25)+1))))

            #Drawing the BosCube scene
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
            if(BossCube_Particles[0].time<200):
                glLibColor((255,255,255,255))
                glTranslated(-1.3,0.6,2)
                BossCube_Level.draw()
                glTranslated(0.76,-0.8,0)
                BossCube_Up.draw()
                glTranslated(0.54,0.2,-2)
                glLibSelectTexture(Texture_Player)

                #If the destroing time of cube 0 under 50 then the scene ends.
                if(BossCube_Particles[0].time<50):
                    BossCube_Particles = []
##                    Prticles_count=BossCube_Particles.__len__()
##                    for i in range(Prticles_count):
##                        BossCube_Particles.pop()
                    BossCube.z=-100
                    Player.a=255

                    #Add one Level and rerender the Level Text
                    Level+=1
                    if(Level==1):
                        Level_Text = glLibObjText("Level 1",Font_ALGER_100,(235,255,0))
                    elif(Level<10):
                        Level_Text = glLibObjText("Level "+str(Level),Font_ALGER_100,(255,255-((Level-1)*20),Level*5))
                    elif(Level==10):
                        Level_Text = glLibObjText("Level X",Font_ALGER_100,(255,0,128))
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

                        #Loading the Text For the End Screen
                        End_Text_1 = glLibObjText("Congratulations",Font_ALGER_100,(255,200,0))
                        End_Text_2 = glLibObjText("You've reached the",Font_ALGER_100,(255,200,0))
                        End_Text_3 = glLibObjText("end of the game",Font_ALGER_100,(255,200,0))
                        End_Text_4 = glLibObjText("Hopefully you had fun",Font_ALGER_100,(255,200,0))
                        End_Text_5 = glLibObjText("and will play it again",Font_ALGER_100,(255,200,0))
                        End_Text_6 = glLibObjText("Enjoy yourself!",Font_ALGER_100,(255,200,0))
                        End_Text_7 = glLibObjText("Nico Bosshard",Font_ALGER_100,(255,200,0))

                        #Prepare the End Screen renderig
                        glDisable(GL_DEPTH_TEST)
                        glLibColor((255,255,255,255))
                        glScalef(0.5,0.5,0.5)

                        z=-40
                        glTranslated(0,0,-40)

                        #End Screen drawing loop
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

                            EndCutscene_key()
                            Window.flip()

                        #Prparing the "The ENd Screen and Loading the Text"
                        #glTranslated(0,0,-100)
                        glScalef(2,2,2)
                        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                        Window.flip()
                        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                        End_Text_8 = glLibObjText("The",Font_ALGER_100,(255,200,0))
                        End_Text_9 = glLibObjText("End",Font_ALGER_100,(255,200,0))
                        glScalef(2,2,2)

                        #"The End" drawing loop
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

                            EndCutscene_key()
                            Window.flip()
                            
                        #Preparing the real colorfull End Screen
                        glTranslated(0,0,20)
                        glScalef(0.5,0.5,0.5)

                        glLibTexturing(False)
                        glLibColor((255,255,255,255))

                        #Generate all the rainbowcolored cubes
                        speed=6
                        for i in range(int(round(1500/speed))):
                            x=random.uniform(-Cube_speed_z[Level-1],Cube_speed_z[Level-1])
                            y=random.uniform(-Cube_speed_z[Level-1],Cube_speed_z[Level-1])
                            z=random.uniform(-Cube_speed_z[Level-1],Cube_speed_z[Level-1])
                            magnitude  = sqrt(x**2 + y**2 + z**2)
                            BossCube_Particles.append(glLibObjBossCube(random.uniform(0.1,0.2),0,0,0,x/magnitude/random.uniform(145,175), y/magnitude/random.uniform(145,175), z/magnitude/random.uniform(145,155),255,0,0,0,2,round(9000/speed)))

                        #glScalef(0.1,0.1,0.1);
                        while (BossCube_Particles[0].time>50):
                            #It was a bug I missed glClear bit it was so beautiful that I let it as it was.
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

                            EndCutscene_key()
                            Window.flip()


                        #glScalef(10,10,10);
                        glEnable(GL_DEPTH_TEST)

                        #Closeing the Game
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

        if(EndlessMode==False and Level_pos>Level_length-110):
            if(Level_pos>Level_length):
                BossScene=True
            else:
                BossPrepare=True

    #The following lines rotates and draws the player. It sould locks as natural as possible.
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


    #the folowing lines are very important! They calculate the FPS Rate and speed up the game so that the game speed is independed of the computer speed and the FPS rate.
    frame_time=time.clock()
    speed=(frame_time-frame_time_alt)*60
    #print speed
    frame_time_alt=frame_time

    #Fliping the Window means nothing then to change between to Buffers. You can imagen to sheets of paper. You draw at once and pu the other on the wall. Now if you are finish drowing you put the new one on the wall und draw over the old one again so that it will be the new one
    #Window.flip()
    pygame.display.flip()

    #If no BossCene is preparing nnd it's time the a new 3x3 cube will be generated.
    if(BossPrepare==False):
        GenerateNewArea_Schutzzeit-=1
        if(GenerateNewArea<0 and GenerateNewArea_Schutzzeit<1):
            GenerateNewArea_Schutzzeit=4
            GenerateCube(GenerateNewArea)

