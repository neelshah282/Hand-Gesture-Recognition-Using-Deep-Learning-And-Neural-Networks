# -*- coding: utf-8 -*-
"""tkinter with opencv with keras model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sNtY87_ZigxbV-6MTLxLWqwE6UxcYFpW

# Load your own model
"""

from keras.models import load_model
model = load_model('E:\SEM-7\Mini Project\Final\mobile_net_model_v1_0-5 (1).h5')
#model.summary() # to see if it is the same as previous

"""# Import packeges"""

import tkinter as tk
import os
import cv2
import sys
from PIL import Image, ImageTk
import numpy
import serial # from serial import serial
import time

"""# Setup bluetooth communication

#bluebooth config

print("Start")
port="/dev/tty.HC-06-DevB" 
#port = "COM*"  #This will be different for various devices and on windows it will probably be a COM port.
bluetooth=serial.Serial(port, 9600)#Start communications with the bluetooth unit
print("Connected")
bluetooth.flushInput() #This gives the bluetooth a little kick

def command(cmd):
    print("Ping")
    bluetooth.write(cmd.encode())
    print("Bytes written")

    #This reads the incoming data. In this particular example it will be the "Hello from Blue" line
    input_data=bluetooth.readline()
    print(input_data.decode())#These are bytes coming in so a decode is needed
    time.sleep(1) #A pause between bursts
    print("Done")
    return 0
"""

"""# Start to build your user interface """

#variable to control two modes
cancel1 = False
cancel2 = True

#==========================================

root = tk.Tk() # create a intergace window
root.title("Hand Gesture Recogniton System By Rahul's Group") # the title of the window
root.geometry('1300x600') # size of the window

canvas = tk.Canvas(root,bg='white',height=150,width=400) # create a 'canvas' area to show some logo pictures
image_path1 = tk.PhotoImage(file='CGPIT.png')
image1 = canvas.create_image(0,0,anchor='nw',image=image_path1)
canvas.place(x=5,y=5) # the location of canvas

# divide the window into 'left' and  'right' two parts
frm_l =tk.Frame(root)
frm_r =tk.Frame(root)

frm_l.pack(side='left')
frm_r.pack(side='right')

#===================================================================
# define all the finctions will be used to react with all 'button'

def hit_me5():
    on_hit = False
    if on_hit == False:
        on_hit =True
        var.set('Move Forward')
        #command("fwd_bit")

def hit_me6():
    on_hit = False
    if on_hit == False:
        on_hit =True
        var.set('Move Backward')
        #command("left_bit")

def hit_me7():
    on_hit = False
    if on_hit == False:
        on_hit =True
        var.set('Move Left')
        #command("right_bit")

def hit_me8():
    on_hit = False
    if on_hit == False:
        on_hit =True
        var.set('Move Right')
        
def hit_me9():
    on_hit = False
    if on_hit == False:
        on_hit =True
        var.set('Stop')
        #command("stop")

def change_cancel2():
    global cancel1,cancel2
    on_hit = False
    if on_hit == False:
        on_hit = True
        if cancel1 == False:
            var.set('Start Gesture Recognition')
            cancel2 = False
            cancel1 = True
            print(cancel1)
        else:
            var.set('Stop Gesture Recognition')
            cancel2 = True
            cancel1 = False
            ini_show_frame()
        
        
#===================================================================
# define the labels and buttons show in your window
# this is the left side, which is the mannual control area

ll = tk.Label(frm_l,text='Manual Control',bg='yellow',font=('Arial',18),width=15,height=2)
ll.pack()

bl1 = tk.Button(frm_l,text='Move Forward',width=15,height=3,command=hit_me5)
bl1.pack(side='top')

bl2 = tk.Button(frm_l,text='Move Left',width=15,height=3,command=hit_me7)
bl2.pack(side='left')

bl3 = tk.Button(frm_l,text='Move Right',width=15,height=3,command=hit_me8)
bl3.pack(side='right')

bl4 = tk.Button(frm_l,text='Move Backward',width=15,height=3,command=hit_me6)
bl4.pack(side='bottom')

bl5 = tk.Button(frm_l,text='Stop',width=15,height=3,command=hit_me9)
bl5.pack(side='bottom')

#===================================================================

lmain = tk.Label(root, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)
lmain.pack()

#===================================================================

# the 'start' botton to change the mode from 'mannual' to 'recognition'
button = tk.Button(frm_l, text="START!", width=15, height=3,command=change_cancel2) 
button.pack(side='bottom')     

#================================

# start load video and show on window
cap = cv2.VideoCapture(0) 
var = tk.StringVar()  

# this is recogniton mode function
def show_frame():
    global var,cancel2
    if cancel2 == False:
        _, frame = cap.read()
        cv2image1 = cv2.flip(frame,1)
        cv2image2 = cv2.cvtColor(cv2image1, cv2.COLOR_BGR2RGBA) # convert video to RGB format  
        
        cv2.rectangle(cv2image2,(360,60),(590,290),(0,255,0),5) # draw square
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(cv2image2,'Put your RIGHT Hand in this square!',(300,40),font,0.6,(0,255,0),2,cv2.LINE_AA)
    
        crop_cv2image = cv2image1[63:287,363:587] # crop the image with size (224,224)
        img = crop_cv2image.reshape((1,)+ crop_cv2image.shape ) #reshape it so that model can accept

        prediction = model.predict(img.reshape(1,224,224,3))[0]                                                      
        pred_class = list(prediction).index(max(prediction))
        print(pred_class)
        
        if pred_class=='ONE':
            var.set('Move Forward')
            #command("fwd_bit")
        elif pred_class=='TWO':
            var.set('Move Backward')
            #command("left_bit")
        elif pred_class=='THREE':
            var.set('Move Left')
            #command("right_bit")
        elif pred_class=='FOUR':
            var.set('Move Right')  
            #command("stop")
        elif pred_class=='FIVE':
            var.set('Stop')  
            #command("stop")

        l = tk.Label(root,textvariable=var,bg='blue',font=('Arial',22),width=25,height=5) # show instruction uder video area
        l.pack(side='bottom')
    
        prevImg = Image.fromarray(cv2image2) # this is the part shows on video area
        imgtk = ImageTk.PhotoImage(image=prevImg)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        if not cancel2: # if cancel2 is False, continuously show video
            lmain.after(10, show_frame)
#===================================
# this is the main function, which is 'mannual control' mode

def ini_show_frame():
    global var,cancel1 

    _, frame = cap.read()
    cv2image1 = cv2.flip(frame,1)
    cv2image2 = cv2.cvtColor(cv2image1, cv2.COLOR_BGR2RGBA)
    
    
    cv2.rectangle(cv2image2,(360,60),(590,290),(0,255,0),5)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(cv2image2,'Put your RIGHT then click START!',(320,40),font,0.6,(0,255,0),2,cv2.LINE_AA)
    
    crop_cv2image = cv2image1[63:287,363:587]

    img = crop_cv2image.reshape((1,)+ crop_cv2image.shape ) 
    
    l = tk.Label(root,textvariable=var,bg='blue',font=('Arial',22),width=25,height=5)
    l.pack(side='bottom')
    
    prevImg = Image.fromarray(cv2image2)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    if cancel1 == False: # if 'start' botton is clicked, cancel1 is True
        lmain.after(10, ini_show_frame)
    else: # start recognition mode
        show_frame()
        
ini_show_frame() # call the main function

root.mainloop() #*****this is the most important code to show the the window*****