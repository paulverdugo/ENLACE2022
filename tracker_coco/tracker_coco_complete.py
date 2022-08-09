from Imports.camera import Camera
from Imports import front_wheels, back_wheels
from Imports import Servo
import picar
from time import sleep,time
import cv2
import numpy as np
import picar
import os

cam = Camera()
cam.to_position(90,130)
# Show image captured by camera, True to turn on, you will need #DISPLAY and it also slows the speed of tracking

scan_enable         = True
rear_wheels_enable  = True
front_wheels_enable = True
pan_tilt_enable     = True

thres = 0.60 # Threshold to detect object

classNames = []
classFile = "/home/pi/PiCar_ENLACE/tracker5/coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "/home/pi/PiCar_ENLACE/tracker5/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "/home/pi/PiCar_ENLACE/tracker5/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

video=cv2.VideoCapture(0)

SCREEN_WIDTH = 360 #640
SCREEN_HIGHT = 270 #480
video.set(3,SCREEN_WIDTH)
video.set(4,SCREEN_HIGHT)
CENTER_X = SCREEN_WIDTH/2
CENTER_Y = SCREEN_HIGHT/2
SIZE_MIN = SCREEN_HIGHT/8
SIZE_MAX = SCREEN_HIGHT*0.9
SIZE_MAX_TOLERANCE= SIZE_MAX*0.15 #+-

#camera follow mode:
#0 = step by step(slow, stable), 
#1 = calculate the step(fast, unstable)
follow_mode = 0

CAMERA_STEP = 4
CAMERA_X_ANGLE = 20
CAMERA_Y_ANGLE = 20

MIDDLE_TOLERANT = SCREEN_WIDTH/20
PAN_ANGLE_MAX   = 170
PAN_ANGLE_MIN   = 10
TILT_ANGLE_MAX  = 150
TILT_ANGLE_MIN  = 100
FW_ANGLE_MAX    = 90+10
FW_ANGLE_MIN    = 90-10

#scan_pos [pan,tilt]
"""
SCAN_POS = [[90, 130], [90, 130], [90, 130], [90, 130],
            [130, 130], [130, 130], [130, 130], [130, 130],
            [60, 130], [60, 130], [60, 130], [60, 130],
            [30, 130], [30, 130], [30, 130], [30, 130],
            [150, 130], [150, 130], [150, 130], [150, 130],
            ]
"""
SCAN_POS = [[90, 130],[120, 130],[60, 130],[30, 130],[10,130],[150,130],[170,130]]

bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
pan_servo = Servo.Servo(1)
tilt_servo = Servo.Servo(2)
picar.setup()

fw.offset = 0
pan_servo.offset = 10
tilt_servo.offset = 0

bw.speed = 0
fw.turn(90)
pan_servo.write(90)
tilt_servo.write(130)

motor_speed = 60
bw_pace=0.65 #seconds


def main():
    pan_angle = 90              # initial angle for pan
    tilt_angle = 130             # initial angle for tilt
    fw_angle = 90
    scan_count = 0
    while True:
        bw.stop()
        for _ in range(7):
            xC,yC,h=tracker()
            print(xC,yC,h)
            if h > SIZE_MIN:
                break
        
        # scan:
        if h < SIZE_MIN:
            
            bw.stop()
            if scan_enable:
                #bw.stop()
                pan_angle = SCAN_POS[scan_count][0]
                tilt_angle = SCAN_POS[scan_count][1]
                if pan_tilt_enable:
                    pan_servo.write(pan_angle)
                    tilt_servo.write(tilt_angle)
                scan_count += 1
                if scan_count >= len(SCAN_POS):
                    scan_count = 0
            else:
                sleep(0.1)
            
        elif abs(h-SIZE_MAX)>= SIZE_MAX_TOLERANCE:
            if follow_mode == 0:
                if abs(xC - CENTER_X) > MIDDLE_TOLERANT:
                    if xC < CENTER_X:
                        print("left") # person is on left
                        pan_angle += CAMERA_STEP
                        if pan_angle > PAN_ANGLE_MAX:
                            pan_angle = PAN_ANGLE_MAX
                    else:                                         # person is on right
                        print("right")
                        pan_angle -= CAMERA_STEP
                        if pan_angle < PAN_ANGLE_MIN:
                            pan_angle = PAN_ANGLE_MIN
                if abs(yC - CENTER_Y) > MIDDLE_TOLERANT:
                    if yC < CENTER_Y :                             # person is on top
                        print("top")
                        tilt_angle += CAMERA_STEP
                        if tilt_angle > TILT_ANGLE_MAX:
                            tilt_angle = TILT_ANGLE_MAX
                    else:                                         # person is on bottom
                        print("bottom")
                        tilt_angle -= CAMERA_STEP
                        if tilt_angle < TILT_ANGLE_MIN:
                            tilt_angle = TILT_ANGLE_MIN
            else:  #when follow=1
                delta_x = CENTER_X - x
                delta_y = CENTER_Y - y
                #print("x = %s, delta_x = %s" % (x, delta_x))
                #print("y = %s, delta_y = %s" % (y, delta_y))
                delta_pan = int(float(CAMERA_X_ANGLE) / SCREEN_WIDTH * delta_x)
                #print("delta_pan = %s" % delta_pan)
                pan_angle += delta_pan
                delta_tilt = int(float(CAMERA_Y_ANGLE) / SCREEN_HIGHT * delta_y)
                #print("delta_tilt = %s" % delta_tilt)
                tilt_angle += delta_tilt

                if pan_angle > PAN_ANGLE_MAX:
                    pan_angle = PAN_ANGLE_MAX
                elif pan_angle < PAN_ANGLE_MIN:
                    pan_angle = PAN_ANGLE_MIN
                if tilt_angle > TILT_ANGLE_MAX:
                    tilt_angle = TILT_ANGLE_MAX
                elif tilt_angle < TILT_ANGLE_MIN:
                    tilt_angle = TILT_ANGLE_MIN
                
            if pan_tilt_enable:
                pan_servo.write(pan_angle)
                tilt_servo.write(tilt_angle)
            sleep(0.01)
            fw_angle = 180 - pan_angle
            if fw_angle < FW_ANGLE_MIN or fw_angle > FW_ANGLE_MAX:
                fw_angle = ((180 - fw_angle) - 90)/2 + 90
                if front_wheels_enable:
                    fw.turn(fw_angle)
                if rear_wheels_enable:
                    bw.speed = motor_speed
                    #t_end=time()+bw_pace
                    #while time()<t_end:
                        #print("backward")
                        #bw.backward()
                    bw.stop()
            else:
                if front_wheels_enable:
                    fw.turn(fw_angle)
                if rear_wheels_enable:
                    bw.speed = motor_speed
                    t_end=time()+bw_pace
                    while time()<t_end:
                        bw.forward()
                    bw.stop()
        else:
                    bw.stop()
                    
def getObjects(img, thres, nms, draw=True, objects=[]):
    xC=0
    yC=0
    height=0
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        max_score=max(confs.flatten()) #most probable to be person
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects and confidence==max_score:
                objectInfo.append([box,className])
                if (draw):
                    #find center and height of frame to compare to image
                    height=box[3]
                    xC= int(box[0]+(box[2])/2) #xmin + (width)/2
                    yC= int(box[1]+height/2) #ymin + (height)/2
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    print("center: "+str(xC)+" , "+str(yC))
                    cv2.circle(img,(xC,yC),2,color=(0,255,0),thickness=2)

    return xC,yC,height

def tracker():
    
    success, img = video.read()
    xC,yC,height = getObjects(img,0.45,0.2, objects=['person'])
    
    cv2.imshow("Output",img)
    cv2.waitKey(1)
    return xC,yC,height #space left, space right

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        cam.to_position(90,130)
        destroy()
