#Namashi Sivaram, Will Jarvis-Cross, Matt Jarvis-Cross
#Infinity Dungeon.py
#a turn based RPG that focuses around exploring randomy generated dungeons. in the dungeons the player can figth random enemies
#in order to level up, get stronger, learn new moves, and complete the game. the player has access to a main hub from where they can
#enter the dungeon or enter the boss battle depending on where they are in the game. in battle the player can choose what attack they want to
#use then choose what target they want to use it on to deal damage or gain buffs in attack defence or speed.
import glob
from pygame import *
from tkinter import *
from math import *#so I can perform math related functions
from random import *#so I can use random functions

root=Tk()
root.withdraw()
init()
font.init()
#mixer.music.load("music/battletheme.mp3")
titleFont=font.SysFont("Cooper Black",29)


startRect=(400,300,200,100)

frameDelay = 50
attack=False

RED=(255,0,0) #tuple - a list that can not be changed!
GREEN=(0,255,0)
BLUE= (0,0,255)
BLACK=(0,0,0)
WHITE=(255,255,255)
YELLOW=(225,255,0)
PINK=(255,105,180)
BROWN=(79,50,29)

title=titleFont.render("Title!",1,(WHITE))

screen = display.set_mode((608,416))
#a funtion that takes a txt file of #s .s and *s and makes it into a pic
def makemap(file):
    mapimage=Surface((3072,2048))
    infile=open(file,"r").read().strip().split("\n")
    x=len(infile[0])

    y=len(infile)

    xpos=0
    ypos=0
    #replaces different symblos with walls stairs or walkable ground
    for i in range(1,y-1):
        for j in range(1,x-1):

            if infile[i][j]=="#" and infile[i-1][j]=="." and infile[i][j+1]==".":
                tile=image.load("tiles/10.bmp").convert()
            elif infile[i][j]=="#" and infile[i+1][j]=="." and infile[i][j+1]==".":
                tile=image.load("tiles/70.bmp").convert()
            elif infile[i][j]=="#" and infile[i+1][j]=="." and infile[i][j-1]==".":
                tile=image.load("tiles/67.bmp").convert()
            elif infile[i][j]=="#" and infile[i-1][j]=="." and infile[i][j-1]==".":
                tile=image.load("tiles/7.bmp").convert()
            elif infile[i][j]=="#" and infile[i+1][j]=="#" and infile[i][j+1]=="#" and infile[i+1][j+1]==".":
                tile=image.load("tiles/4.bmp").convert()
            elif infile[i][j]=="#" and infile[i][j+1]=="#" and infile[i][j-1]=="#" and infile[i+1][j]==".":
                tile=image.load("tiles/5.bmp").convert()
            elif infile[i][j]=="#" and infile[i][j-1]=="#" and infile[i+1][j]=="#" and infile[i+1][j-1]==".":
                tile=image.load("tiles/6.bmp").convert()
            elif infile[i][j]=="#" and infile[i][j-1]=="." and infile[i-1][j]=="#" and infile[i+1][j]=="#":
                tile=image.load("tiles/26.bmp").convert()
            elif infile[i][j]=="#" and infile[i-1][j]=="#" and infile[i][j-1]=="#" and infile[i-1][j-1]==".":
                tile=image.load("tiles/46.bmp").convert()
            elif infile[i][j]=="#" and infile[i][j-1]=="#" and infile[i][j+1]=="#" and infile[i-1][j]==".":
                tile=image.load("tiles/45.bmp").convert()
            elif infile[i][j]=="#" and infile[i-1][j]=="#" and infile[i][j+1]=="#" and infile[i-1][j+1]==".":
                tile=image.load("tiles/44.bmp").convert()
            elif infile[i][j]=="#" and infile[i-1][j]=="#" and infile[i+1][j]=="#" and infile[i][j+1]==".":
                tile=image.load("tiles/30.bmp").convert()
            elif infile[i][j]==".":
                randtile=randrange(0,4)
                tile=image.load("tiles/%i.bmp" %(randtile)).convert()
            elif infile[i][j]=="#" and infile[i+1][j]=="#" and infile[i-1][j]=="#" and infile[i][j+1]=="#" and infile[i][j-1]=="#" :
                tile=image.load("tiles/28.bmp").convert()
            elif infile[i][j]=="*":
                tile=image.load("tiles/55.bmp").convert()
            tile=transform.smoothscale(tile,(32,32))
            mapimage.blit(tile,(j*32,i*32))

    print("done")
    image.save(mapimage,"maptest.png")
    #same as makeMap but makes a mask of just colours(walkable not walkable)
def makemask(file):
    maskimage=Surface((3072,2048))
    infile=open(file,"r").read().strip().split("\n")
    x=len(infile[0])
    y=len(infile)
    for i in range(1,y-1):
        for j in range(1,x-1):
            if infile[i][j]=="#":
                draw.rect(maskimage,(0,255,0),(j*32,i*32,32,32),0)
            elif infile[i][j]=="*":
                draw.rect(maskimage,(0,0,0),(j*32,i*32,32,32),0)
            else:
                draw.rect(maskimage,(255,255,255),(j*32,i*32,32,32),0)
    image.save(maskimage,"dungeonmask.png")
#determines whether the space ahead is walkable and whether its a portal
def clear(x,y):
    global roompic,roommask,roomx,roomy,inroom,inhub,xpos,ypos,mask,po,floor,boss
    WALL=(0,255,0,255)

    #if the place to move to is greater or smaller than the map or its a wall
    if x<0 or x >= mask.get_width() or y<0 or y >= mask.get_height() or maskscreen.get_at((x,y))==(0,255,0,255) or maskscreen.get_at((x,y))==(1,255,1,255):
        return False
    #if its clear or a portal
    elif maskscreen.get_at((x,y))==(0,0,0,255) or maskscreen.get_at((x,y))==(247,213,20,255) or maskscreen.get_at((x,y))==(165, 196, 201, 255):
        if maskscreen.get_at((x,y))==(165, 196, 201, 255):#if its to the final boss
            #initiates boss battle
            inhub=False
            boss=True

            intro(1,2)

        else:#if its to the dungeon
            #makes a new dungeon floor
            screen.fill((255,255,255))
            fonts(Hfont,20,400,"LOADING")
            themap=dungeon()
            themap.mapgrid(96,64,13)
            makemap("map.txt")
            makemask("map.txt")
            mask=image.load("dungeonmask.png").convert()
            po=image.load("maptest.png").convert()
            xpos=-1238
            ypos=-832
            floor+=1
            inhub=False
    #if its a portal
    elif str(maskscreen.get_at((x,y))) in portalsL:

        #loads the map and its blit pos from a txt file
        roompic=image.load(portalsL[portalsL.index(str(maskscreen.get_at((x,y))))+1])
        roommask=image.load(portalsL[portalsL.index(str(maskscreen.get_at((x,y))))+2])
        xpos,ypos=int(portalsL[portalsL.index(str(maskscreen.get_at((x,y))))+3]),int(portalsL[portalsL.index(str(maskscreen.get_at((x,y))))+4])
        inroom=True
        return False
    else:
        return True
#a funciton that creates a randomly generated map
class dungeon:
    def __init__(self):
        self.hallpiece=[8,9,10,13,15]#list of hallway pieces
        self.roomsz=[6,8]#possible room sizes
        self.rooms=[]#list of rooms created with there pos and dimensions
        self.loopL=[]#list of rooms and corridors to branch off of
        self.dire=[0,1,2,3]#list of directions
    def mapgrid(self,xsize,ysize,mrooms):
        self.mrms=mrooms
        self.xsz=xsize
        self.ysz=ysize
        shuffle(self.hallpiece)
        #makes a 2d list of 0s
        self.grid=[[0 for x in range(xsize)]for y in range(ysize)]
        for y in range(7):
            for x in range(7):
                #creates the first room in the middle of the 2d list/map
                self.grid[ysize//2-3+y][xsize//2-3+x]=1
        self.rooms.append([xsize//2-3,ysize//2-2,5,5])
        shuffle(self.dire)#shuffles possibl directiosn for exit
        for i in range(randrange(1,5)):#for a random no of halls
            ex,ey,d=self.findexit(self.rooms[0][0],self.rooms[0][1],self.rooms[0][2],self.rooms[0][3],self.dire[i])#finds an exit for a branch from a room
            xl,yl,d=self.makecorridor(d)#makes a corridor woth its lenght and width and direction

            xp,yp,xl,yl,exx,eyy,d,place=self.placecorridor(ex,ey,xl,yl,d)#places the corridor with the exit
        while len(self.loopL)!=0 and len(self.rooms)!=self.mrms:#continues the branching until it has gone through every room/hall or till max rooms is achived
            self.loop(self.loopL[0][0],self.loopL[0][1],self.loopL[0][2],self.loopL[0][3])

        self.placecamp()#places the stairs in the dungoen
        self.mapfile()#makes it into a file
    def placeroom(self,xpos,ypos,xlen,ylen,di):#places a room in the map
        #uses the direction to determine
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

        if xpos>2 and ypos>2 and xpos+xlen-1<self.xsz-3 and ypos+ylen-1<self.ysz-3:
            self.rooms.append([xpos,ypos,xlen,ylen])
            for y in range(ylen):
                for x in range(xlen):

                    self.grid[ypos+y][xpos+x]=1
        yn=1
        return xpos,ypos,xlen,ylen,yn
    def makeroom(self):# makes a room with varying heights and widths
        shuffle(self.roomsz)#mixes possible dimensions and gets random heights and widths
        xlen=self.roomsz[0]
        shuffle(self.roomsz)
        ylen=self.roomsz[0]
        return xlen,ylen
    def findexit(self,xpos,ypos,xlen,ylen,direct):# finds an exit in the room or corridor
        if direct==0:#north
            xexit=xpos+(xlen%2+xlen//2)-1#gets the middle of the room as an exit
            yexit=ypos-1#exit is top of room
        elif direct==1:#east
            yexit=ypos+(ylen%2+ylen//2)-1#exit is on right wall middle
            xexit=xpos+xlen-1#exit is at end of room
        elif direct==2:#south
            xexit=xpos+(xlen%2+xlen//2)-1#exit is at botom middle
            yexit=ypos+ylen-1#exit is at bottom of room
        elif direct==3:#west
            yexit=ypos+(ylen%2+ylen//2)-1
            xexit=xpos-1
        return xexit,yexit,direct
    def placecorridor(self,xpos,ypos,xlen,ylen,direct):#places a corridor
        rt=1#room type is a corridor
        endx=xpos+xlen-1#end of corridor is at end of it
        endy=ypos+ylen-1
        placed=True#it was sucessfully placed
        #redetermines xpos ypos xends and yends as sometimes direction could be left or up as xpos and ypos should be top left coordinates
        if direct==0:
            ypos-=(ylen-1)
            endy=ypos
        elif direct==3:
            xpos-=(xlen-1)
            endx=xpos
        if xpos<2 or ypos<2 or endx>self.xsz-3 or endy>self.ysz-3:#if the room dosn't fit
            placed=False#it wasn't placed
        if placed:
            self.loopL.append([endx,endy,rt,direct])#adds it to halls to be branched
            #turns those places in the map to walkable spaces .s
            for y in range(ylen):
                for x in range(xlen):
                    self.grid[ypos+y][xpos+x]=1
        return xpos,ypos,xlen,ylen,endx,endy,direct,placed

    def makecorridor(self,direct):#makes a corridor similar to makeroom
        #shuffle possible hall dimensions then gets a random direction as well as dimensions
        shuffle(self.hallpiece)
        xlen,ylen=1,1#one dimension will always be 1 as its a hall
        if direct==0:
            ylen=self.hallpiece[0]
        elif direct==1:
            xlen=self.hallpiece[0]
        elif direct==2:
            ylen=self.hallpiece[0]
        elif direct==3:
            xlen=self.hallpiece[0]
        return xlen,ylen,direct
    def loop(self,etx,ety,rt,direction):#loops thorugh rooms to branch
        if len(self.rooms)==self.mrms:#if max rooms is achived
            return
        if rt==1:#if its a hall
            direct=[0,1,2,3]
            for j in direct:
                if j==direction:#if the direction for the new hall is the same as the one to be branched from
                    pass
                elif j%2==direction%2:#if its back in the same direction as the one to be branched from or the same direction
                    direct.remove(j)#removes it from possible directions
            shuffle(direct)
            r=randrange(100)
            if r<30:#30% chance of branch being a hall
                delloop=False
                tryloop=True
                for i in range(0,randrange(1,3)):#random number of branches
                    for l in direct:
                        x,y,dire=self.makecorridor(l)#makes corridor branch
                        xp,yp,xl,yl,ex,ey,d,place=self.placecorridor(etx,ety,x,y,dire)#tries to place it
                        if place:
                            delloop=True
                            tryloop=False
                            self.loopL.append([ex,ey,1,d])
                if delloop or tryloop:#if it was placed or couldn't be placed
                    del self.loopL[0]#deletes it from rooms to be branched from
            else:#70% chance of branch to be room
                xll,yll=self.makeroom()#makes room
                xpp,ypp,xlll,ylll,pl=self.placeroom(etx,ety,xll,yll,direction)#tries to place it
                if pl:#if placed
                    del self.loopL[0]#deletes it from list
                    for i in range(0,randrange(1,3)):#random numer of branhes
                        for l in direct:
                            exx,eyy,ddd=self.findexit(xpp,ypp,xlll,ylll,l)#finds a exit
                            self.loopL.append([exx,eyy,0,ddd])#adds it to rooms to be branchd from
        else:#if the branch was a room
            xlll,ylll,ddd=self.makecorridor(direction)
            xp,yp,xl,yl,exx,eyy,d,place=self.placecorridor(etx,ety,xlll,ylll,ddd)
            del self.loopL[0]
            #tries to add corridor then delets the room from the loop
    def placecamp(self):#places stairs

        x,y,w,h = choice(self.rooms)#gets dimensions of random room
        campX = randint(x+1,x+w-1)
        campY = randint(y+1,y+h-1)
        self.grid[campY][campX]=3
        #places camp randomly in room

    def mapfile(self):
        #goes through map and turns it into a txt file
        file=open("map.txt","w")
        for y in range(self.ysz):
            line = ""
            for x in range(self.xsz):
                if self.grid[y][x]==1:
                    line += "."
                if self.grid[y][x]==0:
                    line += "#"
                if self.grid[y][x]==3:
                    line+="*"
            file.write("%s\n" %(line))
        file.close()



def moveGuy():#determines directio of move of character
    ''' moveMario controls the location of Mario as well as adjusts the move and frame
        variables to ensure the right picture is drawn.
    '''
    global move, frame, GuyX, GuyY, newMove,xpos,ypos,attack
    keys = key.get_pressed()
    #checks if the place you are trying to move into is a wall or a walkable place
    newMove = -1
    if keys[K_d] and clear(298+17,208):
        newMove = RIGHT
        xpos-=3
    elif keys[K_s] and clear(306,192+32):
        newMove = DOWN
        ypos-= 3
    elif keys[K_w] and clear(306,192-1):
        newMove = UP
        ypos += 3
    elif keys[K_a] and clear(306-1,208):
        newMove = LEFT
        xpos += 3


    else:

        frame = 0

    if move == newMove:     # 0 is a standing pose, so we want to skip over it when we are moving

        frame = frame + 0.2 # adding 0.2 allows us to slow down the animation
        if frame >= len(pics):
            frame = 1
    elif newMove != -1:     # a move was selected
        move = newMove      # make that our current move
        frame = 1




def makeMove(folder,name,start,end):#gets a list of pictures for animations
    ''' This returns a list of pictures. They must be in the folder "name"
        and start with the name "name".
        start, end - The range of picture numbers
    '''
    move = []
    for i in range(start,end+1):
        move.append(image.load("%s/%s (%d).png" % (folder,name,i)))
    return move


def drawScene(image,mask,newMove):#draws the scene after movement

    global xpos, ypos, GuyX, GuyY,move,attack,pics
    screen.blit(image,(xpos,ypos))
    maskscreen.blit(mask,(xpos,ypos))


    if move<=3:
        pics = makeMove("walk2","walk",move*9+1,move*9+8)
        pic=pics[int(frame)]

        screen.blit(pic,(298,192))





    else:
        otherFrame=1



        if attack:


            while otherFrame<=6:
                screen.blit(image,(xpos,ypos))
                if move==FIGHTLEFT:
                    pics = makeMove("fight/fightleft","fightleft",1,6)
                    pic=pics[int(otherFrame)]
                    screen.blit(pic,(412-65,300))
                elif move==FIGHTDOWN:
                    pics = makeMove("fight/fightdown","fightdown",1,6)
                    pic=pics[int(otherFrame)]
                    screen.blit(pic,(412-20,300))
                elif move==FIGHTRIGHT:
                    pics = makeMove("fight/fightright","fightright",1,6)
                    pic=pics[int(otherFrame)]
                    screen.blit(pic,(412-20,300))
                elif move==FIGHTUP:
                    pics = makeMove("fight/fightup","fightup",1,6)
                    pic=pics[int(otherFrame)]
                    screen.blit(pic,(412-25,300-20))

                maskscreen.blit(mask,(xpos,ypos))
                otherFrame+=0.05



        else:
            pics = makeMove("walk","walk",(move-4)*9+1,(move-4)*9+8)
            pic=pics[0]
            screen.blit(pic,(298,192))
            #screen.blit(image,(xpos,ypos))
            maskscreen.blit(mask,(xpos,ypos))
            display.flip()


        attack=False





    return xpos, ypos

#Loading Font
font.init()
Hfont = font.SysFont("Harrington Regular.ttf", 15)
###
def learnmove(player,movechange):#if you are leaning a new move
    global learningmove,info,cinfo,cinfo2

    #gets the info of charecter learning move
    if player==0:
        info=cinfo
    else:
        info=cinfo2
    #you click on different moves to foreget them then function replaces it with new move
    if attackrect1.collidepoint(mx,my) and click:
        forgotmove=info[5]
        info[5]=movechange
        learningmove=False
    if attackrect2.collidepoint(mx,my) and click:
        forgotmove=info[6]
        info[6]=movechange
        learningmove=False
    if attackrect3.collidepoint(mx,my) and click:
        forgotmove=info[7]
        info[7]=movechange
        learningmove=False
    if attackrect4.collidepoint(mx,my) and click:
        forgotmove=info[8]
        info[8]=movechange
        learningmove=False
    if learningmove==False:#once you have chosen a move to forget
        screen.blit(fightwordspic,(0,291))
        fonts(Hfont,50,341,"You forgot %s and learned %s" %(forgotmove,movechange))
        time.wait(1000)
        #updates player infos
        if player==0:
            cinfo=info
        else:
            cinfo2=info

def levelup(player):#if character has increased in level
    global cinfo,cinfo2,php,php2,playeraccess,movelearning,learningmove
    #gets charecter info
    if player==0:
        info=cinfo
    else:
        info=cinfo2
    info[9]=str(int(info[9])+1)#adds 1 to players level
    for i in range(1,5):
        info[i]=levelupstats[int(info[9])-1][player][i-1]
    if levelupstats[int(info[9])-1][player][4]!="x":#if at that level you learn a new move
        if "--" in info:#if you have empty move slots
            pos=info.index("--")
            info[pos]=levelupstats[int(info[9])-1][player][4]
        else:#calls learnmove to replace old moves
            screen.blit(fightwordspic,(0,291))
            fonts(Hfont,50,341,"You are trying to learn %s, but your moves are full. Select a move to change." %(levelupstats[int(info[9])-1][player][4]))
            display.flip()
            time.wait(10000)
            screen.blit(specialmenu,(0,291))
            fonts(Hfont,46,320,info[5])
            fonts(Hfont,187,320,info[6])
            fonts(Hfont,60,585,info[7])
            fonts(Hfont,607,3,info[8])
            movelearning=levelupstats[int(info[9])-1][player][4]
            playeraccess=player
            learningmove=True
    #updates charecter infos
    info[10]=str(int(info[10])-int(info[11]))
    info[11]=str(int(int(info[11])*1.5))
    if player==0:
        cinfo=info
        php=cinfo[1]
    else:
        cinfo2=info
        php2=cinfo2[1]
def exp(lvl):#adds exp from battles to charecters
    global cinfo,cinfo2
    #as long as charecter is not dead gives them exp and if enough exp is obtained levels up charecter
    if php>0:
        cinfo[10]="%i" %(int(cinfo[10])+lvl*2)
        if int(cinfo[10])>=int(cinfo[11]) and int(cinfo[9])<20:
            levelup(0)
    if php2>0:
        cinfo2[10]="%i" %(int(cinfo2[10])+lvl*2)
        if int(cinfo2[10])>=int(cinfo2[11]) and int(cinfo2[9])<20:
            levelup(1)
def enemymoveset(lvl):#makes a random enemy moveset and stats depending on level
    moves=[]
    estats=[]
    randlist=allmoves#randomizes possible moves then chooses moves

    shuffle(randlist)
    if lvl<=20 and lvl>=16:
        for i in range(4):
            moves.append(randlist[i])
        estats.append(randrange(10,40))
        estats.append(randrange(35,50))
        estats.append(randrange(28,38))
        estats.append(randrange(14,20))
        estats.append(randrange(20,26))
        estats.append(randrange(16,20))
    elif lvl<16 and lvl>=10:
        for i in range(3):
            moves.append(randlist[i])
        estats.append(randrange(10,40))
        estats.append(randrange(30,44))
        estats.append(randrange(20,30))
        estats.append(randrange(10,15))
        estats.append(randrange(9,22))
        estats.append(randrange(10,16))

    else:
        for i in range(2):
            moves.append(randlist[i])
        estats.append(randrange(10,40))
        estats.append(randrange(10,28))
        estats.append(randrange(15,20))
        estats.append(randrange(3,7))
        estats.append(randrange(2,10))
        estats.append(randrange(1,10))

    return moves,estats
def eattack(moves):#makes a move for the enemy

    move=moves[randrange(len(moves))]#chooses a random move
    if move in selfincreasemoves:#if the move helps enemy target become the enemy
        targete=3
        targetd=estats[3]
    else:
        #chooses a random target but will only choose ones that are still alive
        targete=randrange(1,3)
        if targete==2:
            targetd=cinfo2[3]
            etxpos,etypos=girlposx,girlposy
            if php2<=0:
                targete=1
                targetd=cinfo[3]
                etxpos,etypos=playerposx,playerposy
        if targete==1:
            targetd=cinfo[3]
            etxpos,etypos=playerposx,playerposy
            if php<=0:
                targete=2
                targetd=cinfo2[3]
                etxpos,etypos=girlposx,girlposy

    specialatk(move,230,230,targete,estats[2],targetd,estats[5],3)
    screen.blit(fightwordspic,(0,291))
    time.wait(1000)
def fonts(name,posx,posy,text):#a function that displays fonts
    txt=(name).render(text, True, (0,0,0))
    screen.blit(txt,(posx,posy))
    display.flip()
#uses a special attack by taking in the attack, the attack recever and the attack user then calculates the dmg dealt or applies special effects of specific moves
#then blits the sprites of the move on the reciver and redrwas the scean with characters that are still alive
def specialatk(name,xpos,ypos,targetatk,attackstat,defence,lvl,moveuser):
    global ehp,php,php2,attacked,p1mp,p2mp,turn,atks,mods
    frincrease=0.1
    frames=0
    copy=screen.copy()
    attack=int(int(attackstat)*mods[moveuser-1][0])
    defence=int(int(defence)*mods[moveuser-1][1])
    lvl=int(lvl)
    atkpower=int(attackstr[allmoves.index(name)])
    userpower=((2*lvl)/5)+2
    adrate=attack/defence
    dmg=(((userpower*atkpower*adrate)/50)+2)
    dmg=int(dmg)#damage to be dealt
    moretext="took %i damage" %(dmg)

    sprites=glob.glob("attacks\\%s\\*.png" %(name))
    if name=="Heat Burst":
        frincrease=0.1
    elif name=="Pixie's Wish":
        dmg=-10
    elif name=="Forest's Breath":
        dmg=-20
    elif name=="Verdant Warping":
        dmg=0
        mods[targetatk-1][2]=min(2,mods[targetatk-1][2]+0.25)
        moretext="speed increased"
    elif name=="Radiant Control":
        dmg=0
        mods[targetatk-1][2]=max(0.25,mods[targetatk-1][1]-0.25)
        moretext="defence decreased"
    elif name=="Psychic Influence":
        dmg=0
        mods[targetatk-1][2]=min(2,mods[targetatk-1][0]+0.25)
        moretext="attack increased"
    elif name=="Mutating Engine":
        dmg=0
        mods[targetatk-1][2]=max(0.25,mods[targetatk-1][2]-0.25)
        moretext="speed decreased"
    elif name=="Charm Ward":
        dmg=0
        mods[targetatk-1][2]=min(2,mods[targetatk-1][1]+0.25)
        moretext="defence increased"
    while frames<len(sprites):
        pic=image.load(sprites[int(frames)])

        screen.blit(copy,(0,0))
        screen.blit(pic,(xpos-(pic.get_width()//2),ypos-(pic.get_height()//2)))
        frames+=frincrease
        display.flip()
    screen.blit(back,(0,0))
    if targetatk==1:
        php=min(php-dmg,int(cinfo[1]))
    elif targetatk==2:
        php2=min(php2-dmg,int(cinfo2[1]))
    elif targetatk==3:
        ehp=min(ehp-dmg,int(estats[1]))
    if php>0:
        screen.blit(playerpics[0],(playerposx,playerposy))
    if php2>0:
        screen.blit(girlwalk[0],(girlposx,girlposy))
    if ehp>0:
        screen.blit(enemypics[0],(eposx,eposy))

    if moveuser<=2:
        screen.blit(fightwordspic,(0,291))
        fonts(Hfont,50,300,("You used %s" %(name)))
        time.wait(2000)
    else:
        screen.blit(fightwordspic,(0,291))
        fonts(Hfont,50,300,("Foe used %s" %(name)))
        time.wait(2000)
    if targetatk==1:
        if php<=0:
            screen.blit(fightwordspic,(0,291))
            fonts(Hfont,50,341,"Girkirat fainted")
            time.wait(4000)
    elif targetatk==2:
        if php2<=0:
            screen.blit(fightwordspic,(0,291))
            fonts(Hfont,50,341,"Karen fainted")
            time.wait(4000)

    else:
        if ehp<=0:
            screen.blit(fightwordspic,(0,291))
            fonts(Hfont,50,341,"Foe fainted")
            time.wait(4000)







#only usable by main characters. deals small damge to enemy and animates character and blits attacks sprites
def attack(pics,standpic,posx,posy,att,defen,user):
    swordslash=0
    attackframe=0
    dmg=int(2+att/defen)
    special = makeMove("Melee 1","Melee 1",1,9)#attak pics
    #player animation
    while swordslash<=5:
        #fswordslash)
        pic=pics[int(swordslash)]
        screen.blit(back,(0,0))
        screen.blit(pic,(posx,posy))
        screen.blit(enemypics[0],(eposx,eposy))
        if user==1 and php2>0:
            screen.blit(girlwalk[0],(girlposx,girlposy))
        elif user==2 and php>0:
            screen.blit(playerpics[0],(playerposx,playerposy))
        swordslash+=0.5
        display.flip()
    #attack's sprites
    while attackframe!=-1:
        pic=special[int(attackframe)]
        screen.blit(back,(0,0))
        if php>0:
            screen.blit(playerpics[0],(playerposx,playerposy))
        if ehp>0:
            screen.blit(enemypics[0],(eposx,eposy))
        if php2>0:
            screen.blit(girlwalk[0],(girlposx,girlposy))
        screen.blit(pic,(eposx,eposy))
        attackframe+=0.25
        if int(attackframe)==len(special):
            attackframe=-1
        display.flip()
    #redrwas scene
    screen.blit(back,(0,0))
    if php>0:
        screen.blit(playerpics[0],(playerposx,playerposy))
    if ehp>0:
        screen.blit(enemypics[0],(eposx,eposy))
    if php2>0:
        screen.blit(girlwalk[0],(girlposx,girlposy))
    display.flip()
def choosetarget():#function for chooseing target. if you click on someones rect they becom the target of theattack
    global target,targetchoose,atargetx,atargety,defencestat
    target=-1
    defencestat=1
    if playerrect.collidepoint(mx,my) and click and php>0:
        target=1
        atargetx,atargety=playerposx,playerposy
        defencestat=cinfo[3]
        targetchoose=False
    elif girlrect.collidepoint(mx,my) and click and php2>0:
        target=2
        atargetx,atargety=girlposx,girlposy
        defencestat=cinfo2[3]
        targetchoose=False
    elif enemyrect.collidepoint(mx,my) and click and ehp>0:
        target=3
        atargetx,atargety=eposx,eposy
        defencestat=estats[3]
        targetchoose=False
    return defencestat
def menu():#master menu for battles
    global ehp,php,php2,battle,specialm,attacked,turn,patk,atargetx,atargety,atks,targetchoose,target,attackpwr,attackerlvl,defencestat,mods,boss
    currentturn=turn
    if turn==2 and php2<=0:
        turn+=1
    elif turn==1 and php<=0:
        turn+=1
    if attacked:
        attacked=False
        turn+=1

    if targetchoose:#if you have to choos a target
        screen.blit(fightwordspic,(0,291))
        specialm=False
        fonts(Hfont,50,300,"Target who?")

        defencestat=choosetarget()#gets the defence stat of the target
        if target!=-1:
            turn+=1
            if turn>2:
                turn=1
    if currentturn!=turn and (target!=-1 or attacked==False):#if player one has already used thier attack makes it player 2's turn

        specialm=False

        atks.append([patk,atargetx,atargety,target,attackpwr,defencestat,attackerlvl])
        target=-1

    if targetchoose==False and target==-1:#if you are choosing wha to do
        #gets character infos
        if turn==1:
            info=cinfo
        else:
            info=cinfo2
        if specialm==False:
            screen.blit(battlemenu,(0,291))
        newmove=-1
        battle=True
        display.flip()

        if ehp<=0:#if enemy is dead ends battle
            exp(int(estats[5]))
            battle=False
            if boss:
                screen.fill((255,255,255))
                fonts(Hfont,298,200,"YOU WIN!!!")
                display.flip()
                time.wait(4000)

        elif (click and specialrect.collidepoint(mx,my)) or specialm:#if you want to use aspecial move

            screen.blit(specialmenu,(0,291))
            specialm=True
            fonts(Hfont,46,320,info[5])
            fonts(Hfont,187,320,info[6])
            fonts(Hfont,46,377,info[7])
            fonts(Hfont,187,377,info[8])
            #adds the atk the place to blit the attack the attacks strength and the attackes lvl to a list called atks that will execute the attack
            if attackrect1.collidepoint(mx,my) and click and info[5]!="--":
                patk,atargetx,atargety,attackpwr,attackerlvl=info[5],383,225,info[2],info[9]
                specialm=False
                targetchoose=True
            if attackrect2.collidepoint(mx,my) and click and info[6]!="--":
                patk,atargetx,atargety,attackpwr,attackerlvl=info[6],383,225,info[2],info[9]
                targetchoose=True
                specialm=False
            if attackrect3.collidepoint(mx,my) and click and info[7]!="--":
                patk,atargetx,atargety,attackpwr,attackerlvl=info[7],383,225,info[2],info[9]
                targetchoose=True
                specialm=False
            if attackrect4.collidepoint(mx,my) and click and info[8]!="--":
                patk,atargetx,atargety,attackpwr,attackerlvl=info[8],383,225,info[2],info[9]
                targetchoose=True
                specialm=False




        elif click and runrect.collidepoint(mx,my):#if you run ends the battle
            if boss:
                screen.blit(fightwordspic,(0,291))
                fonts(Hfont,10,311,"Can't run")
                time.wait(1000)
            else:
                battle=False

        elif click and fightrect.collidepoint(mx,my):#if you want to use a basic atack adds it to the list of attacks to use

            attacked=True
            patk,atargetx,atargety,attackpwr,attackerlvl,defencestat=1,383,225,info[2],info[9],estats[3]

        if battle==False:#ifthe battle is over fades out
            mods=[[1,1,1],[1,1,1],[1,1,1]]
            mixer.music.fadeout(700)
            boss=False
            return
        if len(atks)==3:#if all players have chosen thier attacks

            atkorder=order()#gets the attack order depending on speed

            for i in atkorder:
                #executes attacks in order of list.

                if i=="p1" and php>0 and ehp>0:#if player1's turn to attack
                    if atks[1][0]==1:#1 is a basic attack
                        attack(makeMove("fight/fightright","fightright",1,6),playerpics[0],playerposx,playerposy,atks[1][3],atks[1][5],1)
                    else:#a special attack
                        specialatk(atks[1][0],atks[1][1],atks[1][2],atks[1][3],atks[1][4],atks[1][5],atks[1][6],1)
                    time.wait(1000)
                elif i=="p2" and php2>0 and ehp>0:
                    if atks[2][0]==1:
                        attack(makeMove("sprite/Fattack","Fattack",1,6),girlwalk[0],girlposx,girlposy,atks[2][3],atks[2][5],2)
                    else:
                        specialatk(atks[2][0],atks[2][1],atks[2][2],atks[2][3],atks[2][4],atks[2][5],atks[2][6],2)
                    time.wait(1000)
                elif i=="e" and ehp>0:
                    eattack(emoves)
            atks=["e"]

            turn=1
    #draws hp bars depending on % of hp left for each player
    totalphp=int(cinfo[1])
    totalphp2=int(cinfo2[1])
    totalehp=int(estats[1])
    if php>0:
        screen.blit(hpbar,(playerposx-150,playerposy-50))
        draw.line(screen,(0,255,0),(playerposx-122,playerposy+23),(playerposx-122+max(0,(100//totalphp)*php),playerposy+23),3)
    if php2>0:
        screen.blit(hpbar,(girlposx-150,girlposy-50))
        draw.line(screen,(0,255,0),(girlposx-122,girlposy+23),(girlposx-122+max(0,(100//totalphp2)*php2),girlposy+23),3)
    screen.blit(hpbar,(eposx+60,eposy-50))
    draw.line(screen,(0,255,0),(eposx+88,eposy+23),(eposx+88+max(0,(100//totalehp)*ehp),eposy+23),3)




def order():#gets order of attackers
    speeds=[int(cinfo[4])*mods[0][2],int(cinfo2[4])*mods[1][2],int(estats[4])*mods[2][2]]#list of speed stats * each chareters modifiers from moves
    order=[]
    speeds=sorted(speeds,reverse=True)#sorts them in order of most to least then creates a list of who attacsk first by going through the list of speeds then checking whos speeds they match
    for i in range(len(speeds)):
        if int(cinfo[4])*mods[0][2]==speeds[i] and "p1" not in order:
            order.append("p1")
        elif int(cinfo2[4])*mods[1][2]==speeds[i] and "p2" not in order:
            order.append("p2")
        elif int(estats[4])*mods[2][2]==speeds[i] and "e" not in order:
            order.append("e")
    return order
def intro(encounter,chance):#an animation for when a battle starts
    global battle,emoves,estats,ehp,enemypics,boss


    if battle:#if a battle is already going on
        return

    if (newMove>=0 and newMove<=3) or boss:
        encounter=randrange(encounter)
        #if you encounter something
        if encounter<chance or boss:

            emoves,estats=enemymoveset(int(cinfo[9]))
            ehp=estats[1]
            enemypics=makeMove("enemymove","walk",10,18)
            if boss:# if the encounter is the boss

                emoves=["Psychic Influence","Charm Ward","Trapping Lightning","Fatality Annihilation"]
                estats=[80,90,30,40,30,20]
                ehp=estats[1]
                enemypics=makeMove("enemymove/bosswalk","bosswalk",1,9)
            mixer.music.rewind()
            battle=True

            radius=1
            slow=0
            mixer.music.play(-1,0.2)
            for i in range(4000):#draws a circle for fade in effect
                draw.circle(screen,(0,0,0),(304,208),radius,0)
                slow+=0.2
                if slow==1:
                    radius+=1
                    slow=0
                display.flip()
            posy=-650
            for j in range(130):#slides battle back down from top
                screen.blit(back,(0,posy))
                posy+=5
                display.flip()
            #makes all charecters run in from sides of screen
            cxpos=0
            expos=608
            mframe=0
            while True:

                screen.blit(back,(0,0))

                if php>0:
                    screen.blit(playerpics[int(mframe)],(cxpos,225))
                if php2>0:
                    screen.blit(girlwalk[int(mframe)],(cxpos,175))
                screen.blit(enemypics[int(mframe)],(expos,225))
                mframe+=1
                cxpos+=5
                expos-=5
                if cxpos==220:
                    mframe=0
                if int(mframe)==8:
                    mframe=0.6
                if cxpos==225:
                    break
                display.flip()
            menu()#calls main battle menu

#    def backround(location):
 #       if location=="cave":
  #          backround

RIGHT = 3 # These are just the indicies of the moves
DOWN = 2
UP = 0
LEFT = 1
FIGHTRIGHT=7
FIGHTDOWN=6
FIGHTUP=4
FIGHTLEFT=5

#pics = []
#pics.append(makeMove("walk",28,36))      # RIGHT
#pics.append(makeMove("walk",19,27))     # DOWN
#pics.append(makeMove("walk",1,9))    # UP
#pics.append(makeMove("walk",10,18))    # LEFT

#pics.append(makeMove("walk",43,48))      # RIGHT
#pics.append(makeMove("walk",37,42))     # DOWN
#pics.append(makeMove("walk",49,54))    # UP
#pics.append(makeMove("walk",55,60))    #LEFT

frame=0     # current frame within the move
move=0      # current move being performed
GuyX, GuyY = 400,300
themap=dungeon()
#images
playerpics=makeMove("walk","walk",28,35)# main players pics
girlwalk=makeMove("sprite/femalewalk","femalewalk",1,9)# girls pics
enemypics=makeMove("enemymove","walk",10,18)
back=image.load("battleback/back39.jpg")#battle backround
back=transform.smoothscale(back,(608,416))
battlemenu=image.load("battleback/battlemenu.png")#menu for battles
specialmenu=image.load("battleback/fightmenu.png")#list of moves menu for battle
fightwordspic=image.load("battleback/fightmenuwords.png")# blank menu for blitting txt
hpbar=image.load("slider.png")#hp bar
hpbar=transform.smoothscale(hpbar,(125,150))
hub=image.load("map.png")#hubs map
hub=transform.smoothscale(hub,(3200,3200))
hubmask=image.load("hub.png")#hubs mask
hubmask=transform.smoothscale(hubmask,(3200,3200))
instruct=image.load("images/instructions.png")
playpic=image.load("images/playGame.png")
balloons=image.load("images/balloons.png")
castle=image.load("images/castle.png")
player=image.load("images/player.png")
princess=image.load("images/princess.png")
backarrow=transform.smoothscale(image.load("images/backArrow.png"),(50,50))
#####################dungeon creation####################
themap.mapgrid(96,64,13)
makemap("map.txt")
makemask("map.txt")
mask=image.load("dungeonmask.png").convert()
po=image.load("maptest.png").convert()
#####################variables##########################
patk=1# represents what move is being used in battle by player
roompic=""#variable for when player enters room
roommask=""#mask for roompic
roomx,roomy=0,0#xpos ypos for room images
inroom=False#whether your in a room(building)
playeraccess=0#for when learning new move. tells which player file to access
movelearning=""#used when new move is being learnt
atargetx,atargety=0,0#used to find where to blit attack animations
attackuser=1#used to find who is attacking to calculate damage
attackpwr=1#attack power of move being used
attackerlvl=1#level of attacker
floor=1#to identifly what floor you are on
beaten=0#how many timesyou beat the dungeon
boss=False#if in boss battle
story=False#to bring up story pic
stage=1#to transition from main menu to game
running = True
myClock = time.Clock()
maskscreen=Surface((608,416))#surface for blitting masks
#xpos=-1238#
#ypos=-832
xpos=-464 # x and y pos for blitting maps
ypos=-1124
mapScreen=transform.scale(po,(900,700))
targetchoose=False#to identify who you are attacking
learningmove=False#whther your learning a new move
target=-1#to find whether you have chosen a target yet in choosetarget funtion
battle=False#battle is happening or not
#where to blit pics of charecters
enx,eny=412,290
girlposx,girlposy=225,175
playerposx,playerposy=225,225
eposx,eposy=383,225
newMove=-1#to determine which direcetion you are going to move in
#list of move that are benefical to user
selfincreasemoves=["Charm Ward","Psychic Influence","Verdant Warping","Forest's Breath","Pixie's Wish"]
#level up stats and movesets for characters
levelupstats=[[[9,3,2,4,"Battling Ray"],[7,2,4,3,"Battling Ray"]],[[7,4,1,5,"x"],[8,4,5,1,"Heat Burst"]],[[6,2,2,3,"Heat Burst"],[5,3,3,1,"Gravel Submerge"]],[[3,1,2,7,"x"],[10,2,4,0,"x"]],[[3,4,2,3,"Flashing Axe"],[7,4,4,1,"Verdant Warping"]],[[6,5,3,5,"Chasing Program"],[3,3,2,4,"Pixie's Wish"]],[[8,5,2,6,"x"],[6,4,3,0,"Execution Axe"]],[[2,8,2,3,"Mutating Engine"],[5,3,5,2,"x"]],[[9,4,3,3,"x"],[10,3,3,0,"Twirling Domination"]],[[10,3,2,4,"Tempest Rage"],[8,3,3,1,"x"]],[[6,5,4,4,"x"],[7,4,4,1,"Forest's Breath"]],[[4,3,2,3,"Wrestler Deception"],[6,3,2,2,"Polluting Slice"]],[[6,5,4,3,"x"],[9,3,4,0,"x"]],[[8,4,3,6,"Trapping Lightning"],[8,4,4,1,"Judgement"]]]
specialm=False#if you are using a special attack
cinfo=open("charecter.txt","r").read().strip().split("\n")#character 1s info
portalsL=open("portals.txt","r").read().strip().split(":")#list of portals and rooms and thier info
cinfo2=open("charecter2.txt","r").read().strip().split("\n")#character 2s info
allmoves=open("moveset.txt","r").read().strip().split("\n")#list of moves
attackstr=open("attackstr.txt","r").read().strip().split("\n")#list of move strengths
php=int(cinfo[1])#player 1s hp
php2=int(cinfo2[1])#player 2s hp
ehp=100#enemy's hp
emoves=[]#list for enemy's moves
estats=[]#list for enemy's stats
mods=[[1,1,1],[1,1,1],[1,1,1]]#mods for atk def and spd increases
attacked=False
turn=1#whos turn it is to attack
inhub=True# in the main hub or not

########################rects###########################
playerrect=Rect(playerposx,playerposy,25,50)
girlrect=Rect(girlposx,girlposy,25,50)
enemyrect=Rect(eposx,eposy,25,50)
playrect=Rect(30,300,200,100)
instructionsrect=Rect(378,300,200,100)
storyrect=Rect(548,356,50,50)
backrect=Rect(10,10,50,50)
fightrect=Rect(350,306,100,40)
runrect=Rect(490,306,100,40)
specialrect=Rect(350,361,100,40)
attackrect1=Rect(35,311,100,35)
attackrect2=Rect(165,311,100,35)
attackrect3=Rect(35,366,100,35)
attackrect4=Rect(165,366,100,35)
##################
maskscreen.blit(hubmask,(xpos,ypos))
atks=["e"]

while running:
    click=False
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type==MOUSEBUTTONDOWN:
            if e.button==1:
                click=True
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()

    if stage==1:#the start screen
        #map is background for this scene
        screen.blit(transform.smoothscale(hub,(1200,800)),(0,0))
        draw.rect(screen,(255,0,0),playrect,0)
        draw.rect(screen,(0,0,0),playrect,2)
        draw.rect(screen,(255,0,0),instructionsrect,0)
        draw.rect(screen,(0,0,0),instructionsrect,2)
        screen.blit(transform.smoothscale(instruct,(200,100)),(378,300))
        screen.blit(transform.smoothscale(playpic,(200,100)),(30,300))




        if instructionsrect.collidepoint(mx,my) and click:#instructions page is stage 2
            stage=2

        if playrect.collidepoint(mx,my) and click:#start of the game is stage 3
            stage=3

        display.flip()
    elif stage==2:#instruction screen
        screen.blit(image.load("images/howtoplay.png"),(0,0))
        screen.blit(backarrow,(10,10))
        display.flip()
        if backrect.collidepoint((mx,my)) and click:
            stage=1
    else:#main game

        if floor==11:#if you finished a dungeon
            screen.fill((255,255,255))
            fonts(Hfont,320,208,"DUNGEON COMPLETE")
            time.wait(2000)
            inhub=True
            xpos=-464
            ypos=-1124
            beaten+=1
            if beaten>=20:#if you achived the objective of completing the dungeon 20 times makes hub map include portal to boss
                hub=image.load("map2.png")
                hub=transform.smoothscale(hub,(3200,3200))
                hubmask=image.load("hub2.png")
                hubmask=transform.smoothscale(hubmask,(3200,3200))
                screen.blit(fightwordspic,(0,291))
                fonts(Hfont,10,311,"THE DARKNESS IN THE DUNGEON IS VANQUISHED. HEAD TO THE SOUTH OF TOWN TO BATTLE THE DEMON LORD")
                time.wait(3000)
            php=int(cinfo[1])
            php2=int(cinfo[1])
            floor=1
        if php<=0 and php2<=0:#if you die brings you back to the main map
            boss=False
            battle=False
            inhub=True
            php=int(cinfo[1])
            php2=int(cinfo2[1])
            xpos=-464
            ypos=-1124

        if inhub==False and learningmove==False:#if your in a dungeon keeps on checking for encounters
            intro(250,1)
        if battle:#if you in a battle
            menu()
        elif learningmove:#if your trying to learn a new move

            learnmove(playeraccess,movelearning)
        if battle==False and learningmove==False:#if your walking around
            if storyrect.collidepoint((mx,my)) and click:#if you click on the scroll on the bottom corner
                story=True
            if story:#blits the objective on the screen
                screen.blit(transform.smoothscale(image.load("images/scroll.png"),(200,400)),(200,10))
                screen.blit(backarrow,(10,10))
                if backrect.collidepoint((mx,my)) and click:
                    story=False
            else:#if your not viewing the story lets you move around
                moveGuy()
                if inhub and inroom==False:# in the main hub
                    screen.fill((0,0,0))
                    drawScene(hub,hubmask,newMove)
                    fonts(Hfont,15,10,"DUNGEON BEATEN %i/20" %(beaten))
                elif inroom:# in a room
                    screen.fill((0,0,0))
                    drawScene(roompic,roommask,newMove)
                elif battle ==False and inhub==False:#if in a dungeon
                    drawScene(po,mask,newMove)
                    fonts(Hfont,15,10,"FLOOR %i" %(floor))
                    fonts(Hfont,15,25,"Girkirat LVL: %s" %(cinfo[9]))
                    fonts(Hfont,15,40,"Karen    LVL: %s" %(cinfo2[9]))
            screen.blit(transform.scale(image.load("images/miniScroll.png"),(50,50)),(548,356))

    display.flip()



    myClock.tick(50)


quit()
