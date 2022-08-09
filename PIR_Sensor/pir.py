import RPi.GPIO as GPIO
import socket
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)     #read output from PIR motion sensor
GPIO.setup(13, GPIO.IN)
 
serverAddressPort   = ("100.81.32.131", 20044)
bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

while True:
    i = GPIO.input(11)
    if i==0:                    #when output sensor is LOW
        print ("Pin 11 No intruders")
        msgFromClient = "Pin 11 No intruders"
    elif i==1:                 #when output from motion sensor is HIGH
        print ("Pin 11 Intruder detected")
        msgFromClient = "Pin 11 Intruder detected"
        
    bytesToSend = str.encode(msgFromClient)
    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    sleep(1)
    
    i = GPIO.input(13)
    if i==0:                    #when output sensor is LOW
        print ("Pin 13 No intruders")
        msgFromClient = "Pin 13 No intruders"
    elif i==1:                 #when output from motion sensor is HIGH
        print ("Pin 13 Intruder detected")
        msgFromClient = "Pin 13 Intruder detected"
        
    bytesToSend = str.encode(msgFromClient)
    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    sleep(1)