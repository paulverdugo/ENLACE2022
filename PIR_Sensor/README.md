# PIR (Passive Infrared) Sensor

Two PIR sensors were used in this monitoring system to detect any motion or human movement in the patient’s surrounding environment.

## Setup
For the operation of the PIR sensors a Raspberry pi was used and the code was written in Python (Raspberry pi). Subsequently, UDP communication was used to share the captured information with a mobile robot’s Raspberry Pi board.

If running the exact code in this repository, connect each sensor to its own GND and 5V pins and connect one of them to the GPIO11 pin and the other to GPIO13 pin.

## Results
We tested the sensors in a range of 4m x 2m, where we discovered 90% of their effectiveness when in movement.

The PIR sensor responded with great accuracy, however, it functioned on a very limited range. Because of this, a large number of sensors would be needed to reliably detect movement in a room.

## Smart Phone Notification
PIR sensors were coded in a way that if they detect any human movement or motion, it will send a notification to the cellphone, with the If This Then That App also known as IFTTT App.

To view our **complete results** and **accuracy graphs** please visit our poster [here](https://drive.google.com/file/d/1cZVY9iUgGnpz2CNg0B3yTOZmMcHKgG9y/view?usp=sharing).

#

Made with ❤️ by  Valeria Leal, Mariana Flores, Enya Solis, Paul Verdugo
