import pygame,random,sys
from pygame.locals import *
pygame.init()

window_hight=600
window_width=1200
black=(0,0,0)
white=(255,255,255)
fps=25
lavel=0
addnewflamerate=20
global cactusrect,Canvas,firerect,dragonrect,dragon_img
global moveup,movedown,gravity

class dragon:
    global Canvas,dragonrect,dragon_img
    up=True;
    down=False
    velocity=15
    def __init__(self):
        global Canvas,dragonrect,dragon_img
        dragon_img=pygame.image.load("dragon.png")
        dragonrect=dragon_img.get_rect()
        dragonrect.right=1200
        dragonrect.bottom=550 ##initially above fire

    def update(self):
        global dragonrect,cactusrect,firerect
        if(dragonrect.top<=cactusrect.bottom):
            self.down=True
            self.up=False
        if(dragonrect.bottom>=firerect.top):
            self.down=False
            self.up=True
        if(self.down):
            dragonrect.bottom+=15
        if(self.up):
            dragonrect.top-=15
            
    def get_hight(self):
        return dragonrect.top
        
##end of dragon class    

def terminate():
    pygame.quit();
    sys.exit()
    
def initCanvas():
    global Canvas
    Canvas= pygame.display.set_mode((window_width, window_hight))
    pygame.display.set_caption("mario")
    Canvas.fill(black)

def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                return

def flamehitsmaryo(playerrect,flames):
    
    for f in flames:
        if(f.fireballrect.left<=playerrect.right and f.fireballrect.bottom>=playerrect.top and f.fireballrect.top<=playerrect.bottom ):
            return True
    return False

def drawtext(text,font,surface,x,y):
    textobj=font.render(text,1,white)
    textrect=textobj.get_rect()
    textrect.topleft=(x,y)
    surface.blit(textobj,textrect)

def chk_lavel(Cactusrect,firerect,score):
    global lavel,Canvas
    if(score<(250*lavel)):
        return
    lavel+=1
    Cactusrect.bottom+=20
    firerect.top-=20
    
    
    
class flame:
    
    flamespeed=20
    def __init__(self):
        global dragonrect
        hight=Dragon.get_hight()
        self.fireball_img=pygame.image.load("fireball.png")
        self.fireballrect=self.fireball_img.get_rect()
        self.fireballrect.top=dragonrect.top
        self.fireballrect.left=dragonrect.left

    def update(self):
        self.fireballrect.left-=self.flamespeed

class maryo:
    global moveup,movedown,gravity
    global cactusrect,firerect
    speed=100
    downspeed=20

    def __init__(self):
        global gravity
        self.maryo_img=pygame.image.load("maryo.png")
        self.maryorect=self.maryo_img.get_rect()
        self.maryorect.top=300
        self.maryorect.left=0
        self.score=0
        moveup=movedown=gravity=False
    def update(self):
        global gravity,cactusrect,firerect
        if(moveup and (self.maryorect.top>cactusrect.bottom) and (self.maryorect.top<firerect.top)):
            self.maryorect.top-=self.speed;
            self.score+=20
        elif(movedown and (self.maryorect.top>cactusrect.bottom) and (self.maryorect.top<firerect.top)):
            self.maryorect.bottom+=self.speed;
            self.score+=20
        elif(gravity and (self.maryorect.top>cactusrect.bottom) and (self.maryorect.top<firerect.top)):
            self.maryorect.bottom+=self.downspeed;
        
        
        
mainClock = pygame.time.Clock()
initCanvas()

font=pygame.font.SysFont(None, 28)
#scorefont=
start_img=pygame.image.load("start.png")
startrect=start_img.get_rect()
startrect.centerx=600
startrect.centery=300
    

cactus_img=pygame.image.load("cactus_briks.png")
cactusrect=cactus_img.get_rect()
cactusrect.bottom=50
cactusrect.left=0
        

fire_img=pygame.image.load("fire_bricks.png")
firerect=fire_img.get_rect()
firerect.top=550
firerect.left=0

end_img=pygame.image.load("end.png")
endrect=end_img.get_rect()
endrect.centerx=600
endrect.centery=300

Canvas.blit(start_img,startrect)
pygame.display.update()
wait_for_key()
Dragon=dragon()
topscore=0
lavel=1
pygame.mixer.music.load('mario_theme.WAV')
gameover=pygame.mixer.Sound('mario_dies.WAV')
    
while True:
    flame_list=[]
    flameaddcounter=6
    player=maryo()
    firerect.top=550
    firerect.left=0
    cactusrect.bottom=50
    cactusrect.left=0
    lavel=1
    Dragon=dragon()
    
    gameover.stop()
    pygame.mixer.music.play(-1)
    
    while True:
    
        flameaddcounter+=1
        
        
        if flameaddcounter==addnewflamerate:
            flameaddcounter=0
            newflame=flame()
            flame_list.append(newflame)


        chk_lavel(cactusrect,firerect,player.score)
        
        for f in flame_list:
            flame.update(f)
            
        for f in flame_list:
            if(f.fireballrect.left<=0):
                 flame_list.remove(f)

        anykeypressed=False #for gravity if no key is pressed then maryo should come down automaticaly

        for event in pygame.event.get():
            anykeypressed=True
            if event.type==QUIT:
                terminate()
            if event.type==KEYDOWN:
                if event.key==K_UP:
                    moveup=True
                    movedown=False
                    player.update()
                if event.key==K_DOWN:
                    movedown=True
                    moveup=False
                    player.update()
                elif event.key==K_ESCAPE:
                    terminate()
            elif event.type==KEYUP:
                if event.key==K_ESCAPE:
                    terminate()
            
        if not anykeypressed:  #for gravity
            moveup=False
            movedown=False
            gravity=True
            player.update()
            
                    
        topscore=max(topscore,player.score)        
        Dragon.update()
        Canvas.fill(black)
        Canvas.blit(dragon_img,dragonrect)
        Canvas.blit(cactus_img,cactusrect)
        Canvas.blit(fire_img,firerect)
        Canvas.blit(player.maryo_img,player.maryorect)
        pygame.display.update()
        mainClock.tick(fps)

        drawtext('Score : %s | Top Score : %s |Level : %s' %(player.score,topscore,lavel),font,Canvas,350,cactusrect.bottom+10)
        for f in flame_list:
            Canvas.blit(f.fireball_img,f.fireballrect)
            
        if(flamehitsmaryo(player.maryorect,flame_list)):
            break
        if(player.maryorect.top<=cactusrect.bottom):
            break
        if(player.maryorect.bottom>=firerect.top):
            break
        
            """Canvas.blit(end_img,endrect)
            pygame.display.update()
            wait_for_key()    
            wait_for_key()    
            terminate()"""
            
        
        pygame.display.update()
        mainClock.tick(fps)

    Canvas.blit(end_img,endrect)
    pygame.display.update()
    pygame.mixer.music.stop()
    gameover.play()
    wait_for_key()
        


    
