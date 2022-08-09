import serial
import time
import requests

#define values from sensor
MESSAGE_HEAD = b'\x53' # S
MESSAGE_TAIL = b'\x54' # T

BREATH_RATE_RADAR = b'\x81'
BREATH_DATA = b'\x01'
BREATH_VAL = b'\x02'
BREATH_NORMAL = b'\x01'
BREATH_RAPID = b'\x02'
BREATH_SLOW = b'\x03'
BREATH_DETECTING = b'\x04'
BREATH_INTENSITY = b'\x03'
BREATH_CONFIDENCE = b'\x04'
BREATH_WAVE = b'\x05'

HEART_INF = b'\x85'
RATE_DATA = b'\x01'
RATE_NORMAL = b'\x01'
RATE_RAPID = b'\x02'
RATE_SLOW = b'\x03'
RATE_DETECTING = b'\x04'
HEART_RATE = b'\x02'
RATE_INTENSITY = b'\x03'
RATE_CONFIDENCE = b'\x04'
HEART_RATE_WAVE = b'\x05'

SLEEP_INF = b'\x04'
INOUT_BED = b'\x01'
OUT_BED = b'\x00'
IN_BED = b'\x01'

SLEEP_STATE = b'\x02'
AWAKE = b'\x00'
LIGHT_SLEEP = b'\x01'
DEEP_SLEEP = b'\x02'
SLEEP_NONE = b'\x03'
AWAKE_TIME = b'\x03'
LIGHTSLEEP_TIME = b'\x04'
DEEPSLEEP_TIME = b'\x05'
SLEEP_SCORE = b'\x06'

LOCA_DET_ANOMAL = b'\x07'
OUT_OF_RANGE = b'\x00'
WITHIN_RANGE = b'\x01'

def recvRadarBytes():
    global newData
    recvInProgress = False
    Msg = bytearray()
    ser = serial.Serial("/dev/ttyS0", 115200, timeout=0.5) # Use serial
    # ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.5) # Use USB
    while (ser.inWaiting() > 0 and newData == False) or newData == True:
        rb = ser.read()
        #print(rb)
        
        if recvInProgress == True:
            if rb != MESSAGE_TAIL:  # Not the end of the message
                Msg += rb
                
            else:  # The end of the message
                recvInProgress = False
                Msg += rb
                newData = True
                #print('End of a message!')
                break

        elif rb == MESSAGE_HEAD:
            recvInProgress = True
            Msg = bytearray()
            Msg += rb
            #print('Start of a message!!')
            
    # print('exit the loop...')
    ser.close()
            
    return Msg

def Breath_Heart(Msg):
    #print(Msg)
    #print('Check Msg[2]: ', Msg[2].to_bytes(1, 'big'))
    
    if Msg[2].to_bytes(1, 'big') == BREATH_RATE_RADAR:
        if Msg[3].to_bytes(1, 'big') == BREATH_DATA:
            #pass
            if Msg[6].to_bytes(1,'big') == BREATH_NORMAL:
                print("Radar detects that the current breath rate is normal.")
            elif Msg[6].to_bytes(1,'big') == BREATH_RAPID:
                print("Radar detects that the current breath rate is too fast.")
            elif Msg[6].to_bytes(1,'big') == BREATH_SLOW:
                print("Radar detects that the current breath rate is too slow.")
            elif Msg[6].to_bytes(1,'big') == BREATH_DETECTING:
                print("Radar detects that the current breath rate is detecting.")
            
        elif Msg[3].to_bytes(1, 'big') == BREATH_VAL:
            print("Radar monitored the current breath rate value is ", Msg[6])
            #send notification through IFTTT if BR is out of normal range
            if Msg[6]<12:
                requests.post('https://maker.ifttt.com/trigger/breathrate_low/json/with/key/E9XvcBXWhWEjYYD2-6YEt')
            elif Msg[6]>16:
                requests.post('https://maker.ifttt.com/trigger/breathrate_high/json/with/key/E9XvcBXWhWEjYYD2-6YEt')
        elif Msg[3].to_bytes(1, 'big') == BREATH_INTENSITY:
            print("Radar monitored the current breath intensity value is ", Msg[6])
        elif Msg[3].to_bytes(1, 'big') == BREATH_CONFIDENCE:
            print("Radar monitored the current breath confidence value is ", Msg[6])
        elif Msg[3].to_bytes(1, 'big') == BREATH_WAVE:
            print("The respiratory waveform has not yet been developed.")
            
    elif Msg[2].to_bytes(1, 'big') == HEART_INF:
        if Msg[3].to_bytes(1, 'big') == RATE_DATA:
            if Msg[6].to_bytes(1, 'big') == RATE_NORMAL:
                print("Radar detects that the current heart rate is normal.")
            elif Msg[6].to_bytes(1,'big') == RATE_RAPID:
                print("Radar detects that the current heart rate is too fast.")
            elif Msg[6].to_bytes(1,'big') == RATE_SLOW:
                print("Radar detects that the current heart rate is too slow.")
            elif Msg[6].to_bytes(1,'big') == RATE_DETECTING:
                print("Radar detects that the current heart rate is detecting.")
                
        elif Msg[3].to_bytes(1, 'big') == HEART_RATE:
            print("Radar monitored the current heart rate value is ", Msg[6])
            #send notification through IFTTT if HR is out of normal range
            if Msg[6]<60:
                requests.post('https://maker.ifttt.com/trigger/heartbeat_low/json/with/key/E9XvcBXWhWEjYYD2-6YEt')
            elif Msg[6]>100:
                requests.post('https://maker.ifttt.com/trigger/heartbeat_high/json/with/key/E9XvcBXWhWEjYYD2-6YEt')
        elif Msg[3].to_bytes(1, 'big') == RATE_INTENSITY:
            print("Radar monitored the current heart intensity value is ", Msg[6])
        elif Msg[3].to_bytes(1, 'big') == RATE_CONFIDENCE:
            print("Radar monitored the current heart confidence value is ", Msg[6])
        elif Msg[3].to_bytes(1, 'big') == HEART_RATE_WAVE:
            print("The heart rate waveform has not yet been developed.")
    
    elif Msg[2].to_bytes(1, 'big') == SLEEP_INF:
        if Msg[3].to_bytes(1, 'big') == INOUT_BED:
            if Msg[6].to_bytes(1, 'big') == OUT_BED:
                print("Radar detects someone currently leaving the bed.")
            elif Msg[6].to_bytes(1, 'big') == IN_BED:
                print("Radar detects someone currently in the bed.")
        
        elif Msg[3].to_bytes(1, 'big') == SLEEP_STATE:
            if Msg[6].to_bytes(1, 'big') == AWAKE:
                print("Radar detects that monitored person is awake.")
            elif Msg[6].to_bytes(1, 'big') == LIGHT_SLEEP:
                print("Radar detects that monitored person is in light sleep.")
            elif Msg[6].to_bytes(1, 'big') == DEEP_SLEEP:
                print("Radar detects that monitored person is in deep sleep.")
            elif Msg[6].to_bytes(1, 'big') == SLEEP_NONE:
                print("Radar detects that monitored person nothing.")
                
        elif Msg[3].to_bytes(1, 'big') == AWAKE_TIME:
            print("Radar monitored the awake time is ", Msg[6]&Msg[7])
        elif Msg[3].to_bytes(1, 'big') == LIGHTSLEEP_TIME:
            print("Radar monitored the light sleep time is ", Msg[6]&Msg[7])
        elif Msg[3].to_bytes(1, 'big') == DEEPSLEEP_TIME:
            print("Radar monitored the deep sleep is ", Msg[6]&Msg[7])
        elif Msg[3].to_bytes(1, 'big') == SLEEP_SCORE:
            print("Radar judgement sleep score is ", Msg[6])
    
    elif Msg[2].to_bytes(1, 'big') == LOCA_DET_ANOMAL:
        if Msg[3].to_bytes(1, 'big') == LOCA_DET_ANOMAL:
            if Msg[6].to_bytes(1, 'big') == OUT_OF_RANGE:
                print("Radar detects that the current user is out of monitoring range.")
            elif Msg[6].to_bytes(1, 'big') == WITHIN_RANGE:
                print("Radar detects that the current user is within monitoring range.")
newData=False
def main():
    global newData
    while True:
        try:
            Msg = recvRadarBytes()
        except Exception as e:
            print(e)
        
        if newData == True:
            Breath_Heart(Msg)
            newData = False
if __name__=="__main__":
    main()