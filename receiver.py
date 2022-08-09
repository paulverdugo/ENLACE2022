import socket
import requests

localIP     = "100.81.32.131"
localPort   = 20044
bufferSize  = 1024
msgFromServer="Hello UDP Client"
bytesToSend = str.encode(msgFromServer)
# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
UDPServerSocket.bind((localIP, localPort) )
def receiver():
    break_options=['Pin 11 Intruder detected','Pin 13 Intruder detected','Sensor1: 1Sensor2: 0','Sensor1: 0Sensor2: 1','Sensor1: 1Sensor2: 1']
    print("UDP server up and listening")
    # Listen for incoming datagrams
    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        clientMsg = "Message from Client:{}".format(message)
        clientIP  = "Client IP Address:{}".format(address)
        print(message.decode('utf-8'))
        message = message.decode('utf-8')
        data = message.strip().split(':')
        #sensor1_data = int(data[1][0])
        #sensor2_data = int(data[2][0])
        #print vibration
        #print("Sensor 1: ",sensor1_data,)
        #print("Sensor 2: ",sensor2_data)
        #print PIR
        # Sending a reply to client
        UDPServerSocket.sendto(bytesToSend, address)
        if message in break_options:
            activate=True
            print("break")
            if message==break_options[0] or message==break_options[1]:
                #send notification
                requests.post('https://maker.ifttt.com/trigger/Motion Detected/json/with/key/E9XvcBXWhWEjYYD2-6YEt')
            if message==break_options[2] or message==break_options[3] or message==break_options[4]:
                #send notification
                requests.post('https://maker.ifttt.com/trigger/Movement_Detected/json/with/key/E9XvcBXWhWEjYYD2-6YEt')
            break
    return activate
if __name__=="__main__":
    receiver()