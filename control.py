# picar servo-install
# run in terminal as sudo
import cv2
import keyboard
import picar
from Imports.back_wheels import Back_Wheels
from Imports.front_wheels import Front_Wheels
from Imports.camera import Camera

#start window thread
cv2.startWindowThread()
#get video from default camera
cap=cv2.VideoCapture(0)

picar.setup()
cam = Camera()
back_wheels= Back_Wheels()
front_wheels=Front_Wheels()
run=True
w=100 # forward speed (1-100)
s=70 # backward speed (1-100)
cam.to_position(90,120) #(pan angle,tilt angle)
while True:
    try:
        #read frame
        ret,frame=cap.read()
        frame=cv2.resize(frame,(640,480))
        cv2.imshow('frame',frame)
        if keyboard.is_pressed("up"):
            cam.turn_up()
        if keyboard.is_pressed("down"):
            cam.turn_down()
        if keyboard.is_pressed("left"):
            cam.turn_left()
        if keyboard.is_pressed("right"):
            cam.turn_right()
            
        if keyboard.is_pressed("w"):
            back_wheels.forward()
            back_wheels.speed = w
        elif keyboard.is_pressed("s"):
            back_wheels.backward()
            back_wheels.speed = s
        else: back_wheels.stop()
        
        if keyboard.is_pressed("a"):
            front_wheels.turn_left()
        elif keyboard.is_pressed("d"):
            front_wheels.turn_right()
        else: front_wheels.turn_straight()
        
    except KeyboardInterrupt:
        #return to original position when exit
        cam.to_position(90,130)
        back_wheels.stop()
        front_wheels.turn_straight()
        break