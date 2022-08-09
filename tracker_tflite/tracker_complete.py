import sys
sys.path.insert(1,'/home/pi/PiCar_ENLACE/Imports')
from camera import Camera
import front_wheels, back_wheels
import Servo
sys.path.insert(2,'/home/pi/PiCar_ENLACE/Radar_Sensor')
import heart_breath
import picar
import cv2
import numpy as np
import picar
import os
import serial
from time import time,sleep
import threading

from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision

picar.setup()
cam = Camera()
cam.to_position(90,125)
# Show image captured by camera, True to turn on, you will need #DISPLAY and it also slows the speed of tracking
scan_enable         = True
rear_wheels_enable  = True
front_wheels_enable = True
pan_tilt_enable     = True

# Visualization parameters
row_size = 20  # pixels
left_margin = 24  # pixels
text_color = (0, 0, 255)  # red
font_size = 1
font_thickness = 1

# Initialize the object detection model
base_options = core.BaseOptions(
  file_name='/home/pi/PiCar_ENLACE/tracker_tflite/efficientdet_lite0.tflite', use_coral=False, num_threads=4)
detection_options = processor.DetectionOptions(
  max_results=1, score_threshold=0.5)
options = vision.ObjectDetectorOptions(
  base_options=base_options, detection_options=detection_options)
detector = vision.ObjectDetector.create_from_options(options)

cv2.startWindowThread()
cap=cv2.VideoCapture(0)
out=cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc(*'MJPG'),15.,(320,240))

SCREEN_WIDTH = 640
SCREEN_HIGHT = 480
cap.set(3,SCREEN_WIDTH)
cap.set(4,SCREEN_HIGHT)
CENTER_X = SCREEN_WIDTH/2
CENTER_Y = SCREEN_HIGHT/2
SIZE_MIN = SCREEN_HIGHT/10
SIZE_MAX = SCREEN_HIGHT*0.95
height_tolerance=SCREEN_HIGHT*0.1
#camera follow mode:
#0 = step by step(slow, stable), 
#1 = calculate the step(fast, unstable)
follow_mode = 0

CAMERA_STEP = 2
CAMERA_X_ANGLE = 20
CAMERA_Y_ANGLE = 20

MIDDLE_TOLERANT = 50
PAN_ANGLE_MAX   = 170
PAN_ANGLE_MIN   = 10
TILT_ANGLE_MAX  = 120
TILT_ANGLE_MIN  = 130
FW_ANGLE_MAX    = 90+30
FW_ANGLE_MIN    = 90-30

_MARGIN = 10  # pixels
_ROW_SIZE = 10  # pixels
_FONT_SIZE = 1
_FONT_THICKNESS = 1
_TEXT_COLOR = (0, 0, 255)  # red

#scan_pos [pan,tilt]
SCAN_POS = [[90, 125],[60, 125],[125, 125],[30, 125],[10,125],[150,125],[170,125]]

bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
pan_servo = Servo.Servo(1)
tilt_servo = Servo.Servo(2)

fw.offset = 0
pan_servo.offset = 10
tilt_servo.offset = 0

bw.speed = 0
fw.turn(90)
pan_servo.write(90)
tilt_servo.write(125)

motor_speed = 60



def main():
    pan_angle = 90              # initial angle for pan
    tilt_angle = 125             # initial angle for tilt
    fw_angle = 90

    scan_count = 0
    while True:
        for _ in range(10):
            xC,yC,h = detect('efficientdet_lite0.tflite',4)
            if h > SIZE_MIN:
                break

        #print(xC, yC, h)

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
            
        elif abs(h-SIZE_MAX)>height_tolerance:
            if follow_mode == 0:
                if abs(xC - CENTER_X) > MIDDLE_TOLERANT:
                    if xC < CENTER_X:                              # person is on left
                        pan_angle -= CAMERA_STEP
                        #print("Left   ", )
                        if pan_angle > PAN_ANGLE_MAX:
                            pan_angle = PAN_ANGLE_MAX
                    else:                                         # person is on right
                        pan_angle += CAMERA_STEP
                        #print("Right  ",)
                        if pan_angle < PAN_ANGLE_MIN:
                            pan_angle = PAN_ANGLE_MIN
                if abs(yC - CENTER_Y) > MIDDLE_TOLERANT:
                    if yC < CENTER_Y :                             # person is on top
                        tilt_angle += CAMERA_STEP
                        #print("Top    " )
                        if tilt_angle > TILT_ANGLE_MAX:
                            tilt_angle = TILT_ANGLE_MAX
                    else:                                         # person is on bottom
                        tilt_angle -= CAMERA_STEP
                        #print("Bottom ")
                        if tilt_angle < TILT_ANGLE_MIN:
                            tilt_angle = TILT_ANGLE_MIN
            else: #if follow=1
                delta_x = CENTER_X - xC
                delta_y = CENTER_Y - yC
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
            if abs(xC - CENTER_X) <= MIDDLE_TOLERANT:
                fw_angle = 170-pan_angle
                #print("fw_ang: "+str(fw_angle)+ " pan_ang: "+str(pan_angle))
                """
                if fw_angle < FW_ANGLE_MIN or fw_angle > FW_ANGLE_MAX:
                    fw_angle = ((180 - fw_angle) - 90)/2 + 90
                    if front_wheels_enable:
                        fw.turn(fw_angle)
                    if rear_wheels_enable:
                        bw.speed = motor_speed
                        bw.backward()
                        """
                #else:
                if front_wheels_enable:
                    fw.turn(fw_angle)
                if rear_wheels_enable:
                    bw.speed = motor_speed
                    time_end=time()+1.0 #seconds
                    while time()<time_end:
                        bw.forward()
                    bw.stop()
        else:
            bw.stop()
        
def destroy():
    bw.stop()
    img.release()

def detect(model,num_threads):
    """
    Continuously run inference on images acquired from the camera.
    Args:
    model: Name of the TFLite object detection model.
    camera_id: The camera id to be passed to OpenCV.
    width: The width of the frame captured from the camera.
    height: The height of the frame captured from the camera.
    num_threads: The number of CPU threads to run the model.
    enable_edgetpu: True/False whether the model is a EdgeTPU model.
    """

    #Capture images from the camera and run inference
    success, image = cap.read()
    if not success:
      sys.exit(
          'ERROR: Unable to read from webcam. Please verify your webcam settings.'
      )

    image = cv2.flip(image, 1)

    # Convert the image from BGR to RGB as required by the TFLite model.
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Create a TensorImage object from the RGB image.
    input_tensor = vision.TensorImage.create_from_array(rgb_image)
    # Run object detection estimation using the model.
    detection_result = detector.detect(input_tensor)
    # Draw keypoints and edges on input image
    image,xC,yC,height = visualize(image, detection_result)

    cv2.imshow('object_detector', image)
    
    return xC,yC,height

def visualize(image,detection_result):
    """Draws bounding boxes on the input image and return it.

    Args:
    image: The input RGB image.
    detection_result: The list of all "Detection" entities to be visualize.

    Returns:
    Image with bounding boxes.
    """
    xC=0
    yC=0
    height=0
    for detection in detection_result.detections:
        if detection.classes[0].class_name=="person":
            # Draw bounding_box
            bbox = detection.bounding_box
            start_point = bbox.origin_x, bbox.origin_y
            end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
            cv2.rectangle(image, start_point, end_point, _TEXT_COLOR, 3)
            #find center of frame to compare to center of image
            xC=int(bbox.origin_x+bbox.width/2)
            yC=int(bbox.origin_y+bbox.height/2)
            #find height to compare to max height of frame
            height=bbox.height
            cv2.circle(image,(xC,yC),2,_TEXT_COLOR,3)
            # Draw label and score
            category = detection.classes[0]
            class_name = category.class_name
            probability = round(category.score, 2)
            result_text = class_name + ' (' + str(probability) + ')'
            text_location = (_MARGIN + bbox.origin_x,
                             _MARGIN + _ROW_SIZE + bbox.origin_y)
            cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                        _FONT_SIZE, _TEXT_COLOR, _FONT_THICKNESS)
            
    return image,xC,yC,height
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        cam.to_position(90,125)
        destroy()
