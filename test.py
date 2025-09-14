from tkinter import *
import threading
import time
import random
render_time=0.1
root = Tk()
root.title("HIGHER SKY FOR PYTHON")
root.geometry("640x480")
 
canvas = Canvas(bg="white", width=640, height=480)
canvas.pack(anchor=CENTER, expand=1)

lock=threading.Lock()

skylines=list()#h,x,length
def skylines_generate():
    h=470
    skylines.append([h,0,640])
    for i in range(6):
        h-=random.randrange(20,50)+30
        length=random.randrange(0,100)+100
        skylines.append([h,random.randrange(0,480-length),length])
def skylines_draw():
    for i in skylines:
        canvas.create_line(i[1],i[0],i[1]+i[2],i[0])
class Keys:
    def __init__(self):
        self.left=False
        self.right=False
        self.up=False
        self.down=False

def get_control(h):
    res=0
    for i in reversed(range(len(skylines))):
        if h<skylines[i][0]:
            res=i
            break
    return res   
global keys
keys=Keys()
class Player:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.vy=0
        self.dt=1
        self.lockphys=False
        self.G=80
        self.lineid=0
        self.state="control"
        self.maxjs=70
    def draw(self):
        #with threading.Lock():
        canvas.create_rectangle(self.x-15,self.y,self.x+15,self.y-70,fill="black",outline="black")        
    def move(self,dist):
        #with threading.Lock():
        self.x+=dist
        
    def jump(self,power):
        if self.lockphys:

            self.vy=power
        
        self.lockphys=False
        return 
    def phys_inc(self):
        if self.x<skylines[self.lineid][1] or self.x>skylines[self.lineid][1]+skylines[self.lineid][2]:
            self.lockphys=False
            self.y+=10
        if not self.lockphys:
            self.lineid=get_control(self.y)

        if not self.lockphys:
            self.vy=self.vy-(self.G*self.dt*self.dt)/2
            if self.vy > self.maxjs:
                self.vy=self.maxjs
            if self.vy < -self.maxjs:
                self.vy=-self.maxjs
            self.y=self.y-self.vy*self.dt
        
            if self.y>=skylines[self.lineid][0]:
                self.y=skylines[self.lineid][0]
                self.lockphys=True
                self.vy=0
    def breaks(self):
        if self.lockphys:
            self.y+=10
            self.lockphys=False
global player
player=Player(300,480)



def player_moving():
    if keys.left==True:
        player.move(-10)
    elif keys.right==True:
        player.move(10)
    if keys.up==True:
        player.jump(750)
    if keys.down==True:
        player.breaks()

def keydown(key):
    if key.keysym=="Left":
        keys.left=True
    elif key.keysym=="Right":
        keys.right=True
    elif key.keysym=="Up":
        keys.up=True
    elif key.keysym=="Down":
        keys.down=True
    

def keyup(key):
    if key.keysym=="Left":
        keys.left=False
    elif key.keysym=="Right":
        keys.right=False
    elif key.keysym=="Up":
        keys.up=False
    elif key.keysym=="Down":
        keys.down=False
   

def main():
    return

def render():
    skylines_draw()
    player.draw()
    player.phys_inc()
    player_moving()

def thread_render_m():
    while True:
        render()
        time.sleep(render_time)
        canvas.delete("all")
    
skylines_generate()
frame=Frame(root,width=640,height=480)
root.bind("<KeyPress>",keydown)
root.bind("<KeyRelease>",keyup)
frame.focus_set()

thread_render = threading.Thread(target=thread_render_m)
thread_render.daemon = True 

thread_render.start()

root.mainloop()

