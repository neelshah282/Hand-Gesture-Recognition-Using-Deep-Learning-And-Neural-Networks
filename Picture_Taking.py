#Importing Neccessary Librabries
import numpy as np
import cv2

#Start Video Feed for Capturing some data for Dataset

#Enable your WebCam and Start Video Stream
cap = cv2.VideoCapture(0)

#Counter
i = 1

#Read Video Continuously
while True:
     #Read from the video
    _,frame = cap.read()

    #Flipping the Video Frame
    frame = cv2.flip(frame,1)

    #Drawing a green square which is our ROI where the location of two vertexs are (360,60) and (590,290)
    cv2.rectangle(frame,(360,60),(590,290),(0,255,0),5)

    #Defining Font For Displaying Text
    font = cv2.FONT_HERSHEY_SIMPLEX

    #Writing green text at start at location (255,40)
    cv2.putText(frame,'Put your RIGHT Hand in the Square',(255,40),font,0.7,(0,255,0),2,cv2.LINE_AA)

    #Displaying your video on your computer as name 'Picture Taking'
    cv2.imshow('Taking Gesture Pictures',frame)

    #Getting input from keyboard for invoking the System
    k = cv2.waitKey(1)

    #Press 'c' key to capture photo, and increment counter by 1
    if k == ord('c'):
        i+=1

        #Print out the counter value
        print(i)

        #Saving your picture with size (224,224) to some location in the same folder
        cv2.imwrite('images/train/'+str(i)+'.jpg',frame[63:287,363:587])
          
    #Press 'Esc' key to exit
    if k ==27:
        #Exit while loop
        break
        
#========================================

#Closing All Windows & Disabling the Camera
cv2.destroyAllWindows()
cap.release()
