# Smart Elderly Monitoring with Mobile Robots

This repository contains all the code necessary and some failed attempts of our mobile robot project.

The open source SunFounder PiCar-V was modified and utilized as our mobile robot.

## Introduction
Our goal is to build a smart system that provides consistent and timely support to elder people. We target effective detection of elderly events, as well as their prevention.

We propose a contactless solution for elderly monitoring by equipping a mobile robot with a camera and communicating it with a PIR sensor to detect movement and a vibration sensor to detect falls which the robot will respond to and take action.

## Method

Aside from the complete SunFounder PiCar-V setup, the following hardware was used:
- PIR Sensor (HC-SR501 Module)
- Vibration Sensor (SW-420 Module)
- Radar Sensor (Seeed Studio 60 GHz Heartbeat/Breathing Module)
- ESP 8266 WiFi Module
- Raspberry Pi 3

The proposed algorithm for event detection and response process involves four different steps:
1. Accident detection by any sensor (PIR or vibration).
2. Send signal to mobile robot.
3. Movement to determined location (object detection), vital signs monitoring (Radar Sensor), live video streaming (PiCar camera).
4. Notification sent to care provider.

Each sensor's "sender" code is included inside the specific folder as well as it's readme file elaborating on the sensor setup.

```
.
├── access_cam.py     // access default camera on raspberry pi
├── client.py         // runs complete system
├── control.py        // controls front wheels, back wheels, and camera servos with keyboard (run as sudo)
├── Imports           // contains import files
├── LICENSE
├── PIR_Sensor        // contains code that reads sensor info and sends it to car and notification
├── Radar_Sensor      // contains code that reads sensor info, prints it, and sends notification
├── README.md
├── receiver.py       // receives info from sensors and breaks when one is activated
├── tracker_coco      // contains object detection code and its trained model files (coco ssd)
├── tracker_tflite    // contains object detection code and its trained model files (tensorflow lite)
└── Vib_Sensor        // contains code that reads sensor info and sends it to car and notification
```

There are also two different object detection codes:
1. Coco SSD based [(Link to tutorial)](https://core-electronics.com.au/guides/object-identify-raspberry-pi/)
	- This was a failed attempt because the frame marked around a person detected was not centered correctly, making it very hard for the robot to track.
2. Tensorflow Lite based [(Link to tutorial)](https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi)
	- This was the object detection used in the final product. However, with an average of 1.3 fps, the tracking of the car is somewhat slow and may lose the target with any quick movement, leaving plenty of room for improvement

### Run the Code
When downloaded the complete repository and its requirements:

* To run the robot car: 
```
python3 client.py
```

* To run the human detector:
```
python3 tracker.py
```

* To run the radar sensor
```
python3 heart_breath.py
```

* To run the PIR sensor
```
python3 pir.py
```

* To run the vibration sensor: 

    Upload code into arduino with sensor and computer connected to view values printed

## Results

We ran several tests to determine the accuracy and reliability of our final product.

The **radar sensor** was compared to the readings from an Apple Watch (2nd generation), showing very similar values as well as a quick response.

The **PIR sensor** responded with great accuracy, however, it functioned on a very limited range. Because of this, a large number of sensors would be needed to reliably detect movement in a room.

The **vibration sensor** was the only one that varied its accuracy depending on its location. Showing a better response when placed over a wooden floor.

To view our **complete results** and **accuracy graphs** please visit our poster [here](https://drive.google.com/file/d/1cZVY9iUgGnpz2CNg0B3yTOZmMcHKgG9y/view?usp=sharing).

# 

Made with ❤️ by  Valeria Leal, Mariana Flores, Enya Solis, Paul Verdugo
