from itertools import cycle
from random import randrange
from tkinter import Tk , Canvas, messagebox, font
from PIL import ImageTk
import time
from pygame import mixer


# sunetele aferente
mixer.init()
castigat=mixer.Sound("castigat.wav")
fail=mixer.Sound("pierdut.mp3")
ambiental=mixer.Sound("primavara.wav")
game_over=mixer.Sound("game_over.wav")

# facut fundal
win=Tk()
win.title("AplicatiI Multimedia- ANGHE IULIA IOANA")
ambiental.play()
time.sleep(0.1)

image1 = ImageTk.PhotoImage(file = "C:/Users/Iulia/Documents/AM_proiect/img1.jpg")
image2 = ImageTk.PhotoImage(file="C:/Users/Iulia/Documents/AM_proiect/img2.jpg")
image3 = ImageTk.PhotoImage(file="C:/Users/Iulia/Documents/AM_proiect/img3.jpg")
canvas_width=image1.width()
canvas_height=image1.height()

background=Canvas(win, width= canvas_width, height=canvas_height )
t=background.create_image(0, 0, image = image1,anchor='nw')

#
# background.create_rectangle(-5,canvas_height-100, canvas_width+5,canvas_height+5, fill='sea green', width=0)
background.create_oval(-80,-80,120,120, fill='yellow', width=0)
background.pack()



# egg and catcher

color_cycle=cycle(['black','pink','light pink','purple','light green','blue'])
egg_width=45
egg_height=55
egg_score=10
egg_speed=500
egg_interval=4000
difficulty_factor=0.95


# catcher
catcher_color='brown'
catcher_width=100
catcher_height=100
catcher_start_x=canvas_width/2-catcher_width/2
catcher_start_y=canvas_height-catcher_height-20
catcher_end_x=catcher_start_x+catcher_width
catcher_end_y=catcher_start_y+catcher_height

catcher=background.create_arc(catcher_start_x,catcher_start_y,catcher_end_x,catcher_end_y,start=200,extent=140, style='arc',outline=catcher_color,width=5)



# interfaces SCORE;LEVEL

score=0
score_text=background.create_text(20,20,anchor='nw', font=('Arial',14,'bold'),fill='darkblue',text='Scor: '+str(score))
lives_remaning=3
lives_text=background.create_text(canvas_width-20,20,anchor='ne', font=('Arial',14,'bold'),fill='darkblue',text='Sanse: '+str(lives_remaning))
level=0
level_text=background.create_text(20,40,anchor='nw', font=('Arial',14,'bold'),fill='darkblue',text='Nivel: '+str(level))




# create egg and movements

eggs=[]
def create_eggs():
    x=randrange(10,740)
    y=40
    new_egg=background.create_oval(x,y,x+egg_width,y+egg_height,fill=next(color_cycle),width=0)
    eggs.append(new_egg)
    # creaza un nou ou dupa ce trece timpu tre sa apara altul
    win.after(egg_interval,create_eggs)


def move_eggs():
    for egg in eggs:
        try:
            (egg_x, egg_y, egg_x2, egg_y2) = background.coords(egg)
            background.move(egg, 0, 10)
            if egg_y2 > canvas_height:
                egg_dropped(egg)
        except:
            pass
    win.after(egg_speed, move_eggs)

def egg_dropped(egg):
    eggs.remove(egg)
    background.delete(egg)
    lose_a_life()
    if lives_remaning == 0:
        game_over.play()
        time.sleep(0.5)
        messagebox.showinfo('Ai peirdut!','Scor final:'+ str(score))
        win.destroy()
#     scoatem oul din lista de oua totale si daca vietiile sunt 0 atunci e end game


def lose_a_life():
    global lives_remaning
    lives_remaning -= 1
    fail.play()
    time.sleep(0.5)
    # ca sa ti faca mereu update pe ecran folosim itemconfigure
    background.itemconfigure(lives_text, text='Sanse: '+ str(lives_remaning))


def catch_check():
    (catcher_x, catcher_y, catcher_x2, catcher_y2)=background.coords(catcher)
    for egg in eggs:
        (egg_x, egg_y, egg_x2, egg_y2)= background.coords(egg)
        if catcher_x< egg_x and egg_x2 < catcher_x2 and catcher_y2-egg_y2 < 40:
            eggs.remove(egg)
            background.delete(egg)
            increase_score_level(egg_score)
    win.after(100,catch_check)

def increase_score_level(points):
    global score,egg_speed, egg_interval,level,image3,image1,image2
    score+=points
    castigat.play()
    time.sleep(0.3)
    if score ==30:
        level+=1
        background.itemconfig(t,image=image2)
    elif score==60:
        level+= 1
        background.itemconfig(t, image=image3)
    egg_speed=int(egg_speed * difficulty_factor)
    egg_interval= int(egg_interval * difficulty_factor)
    background.itemconfigure(score_text,text='Scor: '+ str(score))
    background.itemconfigure(level_text, text='Nivel: ' + str(level))





def move_left(event):
    (x1,y1,x2,y2)=background.coords(catcher)
    if x1>0:
        background.move(catcher,-20,0)

def move_right(event):
    (x1, y1, x2, y2) = background.coords(catcher)
    if x1 < canvas_width:
        background.move(catcher, 20, 0)

background.bind('<Left>',move_left)
background.bind('<Right>',move_right)
background.focus_set()


win.after(1000,create_eggs)
win.after(1000,move_eggs)
win.after(1000,catch_check)

win.mainloop()
