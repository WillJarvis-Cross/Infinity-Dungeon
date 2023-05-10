"""
sprite3.py
~~~~~~~~~~
This example demonstrates simple sprite animation without using any "fancy" techniques.

"""
from pygame import *

screen = display.set_mode((850,650))
from random import *
def makemap(file):
    mapimage=Surface((4000,3000))
    infile=open(file,"r").read().strip().split("\n")
    x=len(infile[0])
    print(x)
    y=len(infile)
    print(y)
    xpos=0
    ypos=0
    for i in range(1,y-1):
        for j in range(1,x-1):
            #print(i,j)
            if infile[i][j]=="#" and infile[i-1][j]=="." and infile[i][j+1]==".":
                tile=image.load("tiles/10.bmp")
            elif infile[i][j]=="#" and infile[i+1][j]=="." and infile[i][j+1]==".":
                tile=image.load("tiles/70.bmp")
            elif infile[i][j]=="#" and infile[i+1][j]=="." and infile[i][j-1]==".":
                tile=image.load("tiles/67.bmp")
            elif infile[i][j]=="#" and infile[i-1][j]=="." and infile[i][j-1]==".":
                tile=image.load("tiles/7.bmp")
            elif infile[i][j]=="#" and infile[i+1][j]=="#" and infile[i][j+1]=="#" and infile[i+1][j+1]==".":
                tile=image.load("tiles/4.bmp")
            elif infile[i][j]=="#" and infile[i][j+1]=="#" and infile[i][j-1]=="#" and infile[i+1][j]==".":
                tile=image.load("tiles/5.bmp")
            elif infile[i][j]=="#" and infile[i][j-1]=="#" and infile[i+1][j]=="#" and infile[i+1][j-1]==".":
                tile=image.load("tiles/6.bmp")
            elif infile[i][j]=="#" and infile[i][j-1]=="." and infile[i-1][j]=="#" and infile[i+1][j]=="#":
                tile=image.load("tiles/26.bmp")
            elif infile[i][j]=="#" and infile[i-1][j]=="#" and infile[i][j-1]=="#" and infile[i-1][j-1]==".":
                tile=image.load("tiles/46.bmp")
            elif infile[i][j]=="#" and infile[i][j-1]=="#" and infile[i][j+1]=="#" and infile[i-1][j]==".":
                tile=image.load("tiles/45.bmp")
            elif infile[i][j]=="#" and infile[i-1][j]=="#" and infile[i][j+1]=="#" and infile[i-1][j+1]==".":
                tile=image.load("tiles/44.bmp")
            elif infile[i][j]=="#" and infile[i-1][j]=="#" and infile[i+1][j]=="#" and infile[i][j+1]==".":
                tile=image.load("tiles/30.bmp")
            elif infile[i][j]==".":
                randtile=randrange(0,4)
                tile=image.load("tiles/%i.bmp" %(randtile))
            elif infile[i][j]=="#" and infile[i+1][j]=="#" and infile[i-1][j]=="#" and infile[i][j+1]=="#" and infile[i][j-1]=="#" :
                tile=image.load("tiles/28.bmp")
            tile=transform.smoothscale(tile,(50,50))
            mapimage.blit(tile,(j*50,i*50))

    print("done")
    image.save(mapimage,"maptest.png")
def makemask(file):
    maskimage=Surface((4000,3000))
    infile=open(file,"r").read().strip().split("\n")
    x=len(infile[0])
    y=len(infile)
    for i in range(1,y-1):
        for j in range(1,x-1):
            if infile[i][j]=="#":
                draw.rect(maskimage,(0,255,0),(j*50,i*50,50,50),0)
            else:
                draw.rect(maskimage,(255,255,255),(j*50,i*50,50,50),0)
    image.save(maskimage,"dungeonmask.png")
def clear(x,y):
    WALL=(0,255,0,255)
    if x<0 or x >= mask.get_width() or y<0 or y >= mask.get_height() or maskscreen.get_at((x,y))==(0,255,0,255):
        return False
    else:
        return True
class dungeon:
    def __init__(self):
        self.hallpiece=[8,9,10,13,15]
        self.roomsz=[6,8]
        self.rooms=[]
        self.loopL=[]
        self.dire=[0,1,2,3]
    def mapgrid(self,xsize,ysize,mrooms):
        self.mrms=mrooms
        self.xsz=xsize
        self.ysz=ysize
        shuffle(self.hallpiece)
        self.grid=[[0 for x in range(xsize)]for y in range(ysize)]
        for y in range(7):
            for x in range(7):
                self.grid[ysize//2-3+y][xsize//2-3+x]=1
        self.rooms.append([xsize//2-3,ysize//2-2,5,5])
        shuffle(self.dire)
        for i in range(randrange(1,5)):
            ex,ey,d=self.findexit(self.rooms[0][0],self.rooms[0][1],self.rooms[0][2],self.rooms[0][3],self.dire[i])
            xl,yl,d=self.makecorridor(d)
            print(ex,ey,xl,yl,d)
            xp,yp,xl,yl,exx,eyy,d,place=self.placecorridor(ex,ey,xl,yl,d)
        while len(self.loopL)!=0 and len(self.rooms)!=self.mrms:
            self.loop(self.loopL[0][0],self.loopL[0][1],self.loopL[0][2],self.loopL[0][3])
        self.mapfile()
    def placeroom(self,xpos,ypos,xlen,ylen,di):
        if di==0:
            xpos-=xlen//2
            ypos-=(ylen-1)
            
        elif di==1:
            ypos-=ylen//2
            
        elif di==2:
            xpos-=xlen//2
            
        elif di==3:
            ypos-=ylen//2
            xpos-=(xlen-1)
            
        if xpos>0 and ypos>0 and xpos+xlen-1<self.xsz-2 and ypos+ylen-1<self.ysz-2:
            self.rooms.append([xpos,ypos,xlen,ylen])
            for y in range(ylen):
                for x in range(xlen):
                    
                    self.grid[ypos+y][xpos+x]=1
        yn=1
        return xpos,ypos,xlen,ylen,yn
    def makeroom(self):
        shuffle(self.roomsz)
        xlen=self.roomsz[0]
        shuffle(self.roomsz)
        ylen=self.roomsz[0]
        return xlen,ylen
    def findexit(self,xpos,ypos,xlen,ylen,direct):
        if direct==0:
            xexit=xpos+(xlen%2+xlen//2)-1
            yexit=ypos-1
        elif direct==1:
            yexit=ypos+(ylen%2+ylen//2)-1
            xexit=xpos+xlen-1
        elif direct==2:
            xexit=xpos+(xlen%2+xlen//2)-1
            yexit=ypos+ylen-1
        elif direct==3:
            yexit=ypos+(ylen%2+ylen//2)-1
            xexit=xpos-1
        return xexit,yexit,direct
    def placecorridor(self,xpos,ypos,xlen,ylen,direct):
        rt=1
        endx=xpos+xlen-1
        endy=ypos+ylen-1
        placed=True
        if direct==0:
            ypos-=(ylen-1)
            endy=ypos
        elif direct==3:
            xpos-=(xlen-1)
            endx=xpos
        if xpos<1 or ypos<1 or endx>self.xsz-2 or endy>self.ysz-2:
            placed=False
        if placed:
            self.loopL.append([endx,endy,rt,direct])
            for y in range(ylen):
                for x in range(xlen):
                    self.grid[ypos+y][xpos+x]=1
        return xpos,ypos,xlen,ylen,endx,endy,direct,placed
            
    def makecorridor(self,direct):
        shuffle(self.hallpiece)
        xlen,ylen=1,1
        if direct==0:
            ylen=self.hallpiece[0]
        elif direct==1:
            xlen=self.hallpiece[0]
        elif direct==2:
            ylen=self.hallpiece[0]
        elif direct==3:
            xlen=self.hallpiece[0]
        return xlen,ylen,direct
    def loop(self,etx,ety,rt,direction):
        if len(self.rooms)==self.mrms:
            return
        if rt==1:
            direct=[0,1,2,3]
            for j in direct:
                if j==direction:
                    pass
                elif j%2==direction%2:
                    direct.remove(j)
            shuffle(direct)
            r=randrange(100)
            if r<30:
                delloop=False
                tryloop=True
                for i in range(0,randrange(1,3)):
                    for l in direct:
                        x,y,dire=self.makecorridor(l)
                        xp,yp,xl,yl,ex,ey,d,place=self.placecorridor(etx,ety,x,y,dire)
                        if place:
                            delloop=True
                            tryloop=False
                            self.loopL.append([ex,ey,1,d])
                if delloop or tryloop:
                    del self.loopL[0]
            else:
                xll,yll=self.makeroom()
                xpp,ypp,xlll,ylll,pl=self.placeroom(etx,ety,xll,yll,direction)
                if pl:
                    del self.loopL[0]
                    for i in range(0,randrange(1,3)):
                        for l in direct:
                            exx,eyy,ddd=self.findexit(xpp,ypp,xlll,ylll,l)
                            self.loopL.append([exx,eyy,0,ddd])
        else:
            xlll,ylll,ddd=self.makecorridor(direction)
            xp,yp,xl,yl,exx,eyy,d,place=self.placecorridor(etx,ety,xlll,ylll,ddd)
            del self.loopL[0]
    def mapfile(self):
        file=open("map.txt","w") 
        for y in range(self.ysz):
            line = ""
            for x in range(self.xsz):
                if self.grid[y][x]==1:
                        line += "."
                if self.grid[y][x]==0:
                        line += "#"
            file.write("%s\n" %(line))
        file.close()



def moveGuy():
    ''' moveMario controls the location of Mario as well as adjusts the move and frame
        variables to ensure the right picture is drawn.
    '''
    global move, frame, GuyX, GuyY, newMove,xpos,ypos
    keys = key.get_pressed()

    newMove = -1        
    if keys[K_d] and clear(412+25,325):
        newMove = RIGHT
        xpos-=3
    elif keys[K_s] and clear(424,300+50):
        newMove = DOWN
        ypos-= 3
    elif keys[K_w] and clear(424,300-1):
        newMove = UP
        ypos += 3
    elif keys[K_a] and clear(412-1,325):
        newMove = LEFT
        xpos += 3
    else:
        frame = 0

    if move == newMove:     # 0 is a standing pose, so we want to skip over it when we are moving
        frame = frame + 0.2 # adding 0.2 allows us to slow down the animation
        if frame >= len(pics[move]):
            frame = 1
    elif newMove != -1:     # a move was selected
        move = newMove      # make that our current move
        frame = 1
    

def makeMove(name,start,end):
    ''' This returns a list of pictures. They must be in the folder "name"
        and start with the name "name".
        start, end - The range of picture numbers 
    '''
    move = []
    for i in range(start,end+1):
        move.append(image.load("%s/%s (%d).png" % (name,name,i)))
    return move


def drawScene(image,newMove):
    global xpos, ypos, GuyX, GuyY
    screen.blit(image,(xpos,ypos))
    maskscreen.blit(mask,(xpos,ypos))
    pic = pics[move][int(frame)]
    screen.blit(pic,(412,300))            
    display.flip()
    return xpos, ypos


RIGHT = 0 # These are just the indicies of the moves
DOWN = 1  
UP = 2
LEFT = 3

pics = []
pics.append(makeMove("walk",28,36))      # RIGHT
pics.append(makeMove("walk",19,27))     # DOWN
pics.append(makeMove("walk",1,9))    # UP
pics.append(makeMove("walk",10,18))    # LEFT

frame=0     # current frame within the move
move=0      # current move being performed
GuyX, GuyY = 400,300
themap=dungeon()
themap.mapgrid(80,60,13)
makemap("map.txt")
makemask("map.txt")
mask=image.load("dungeonmask.png")
po=image.load("maptest.png")
running = True
myClock = time.Clock()
maskscreen=Surface((850,650))
screen.blit(po,(-1588,-1200))
maskscreen.blit(mask,(-1588,-1200))
xpos=-1588
ypos=-1200
while running:
    for evnt in event.get():
        if evnt.type == QUIT:
            running = False

    moveGuy()
    
    drawScene(po,newMove)

    myClock.tick(50)
    
quit()
