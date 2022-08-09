# Vibration Sensor

Two SW-420 vibration sensors were used in this monitoring system to identify any falls or sudden movements that the elderly person may have.

## Setup

For the operation of the vibration sensors an ESP8266 WiFi Module was used and the code was written in Arduino. Subsequently, UDP communication was used to share the captured information with a Raspberry Pi board.

If running the exact code in this repository, connect each sensor to it's own GND and 3.3V pins and connect one of them to the GPIO4 pin and the other to GPIO5 pin.

## Results

We tested them on different surfaces and at distances of 0.30 meters and 0.90 meters from the sensors to the vibration.

The surfaces were:
- Wooden floors.
- Concrete floors.
- Metal surfaces.
- Walls
- Doors

We observed that, in most cases, the sensors that were 0.30 meters away from the vibration picked up 10% more accuracy than sensors that were 0.90 meters away.
At the end vibration sensor accuracy averages were 60% for those tested at 0.30 meters distance and 48% for those tested at 0.90 meters.

## Smart Phone Notification
Vibration sensors were coded in a way that if they detect any irregular movement or vibration, it will send a notification to the cellphone, with the If This Then That App also known as IFTTT App.

# 

To view our **complete results** and **accuracy graphs** please visit our poster [here](https://drive.google.com/file/d/1cZVY9iUgGnpz2CNg0B3yTOZmMcHKgG9y/view?usp=sharing).

#

Made with ❤️ by  Valeria Leal, Mariana Flores, Enya Solis, Paul Verdugo
