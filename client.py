import sys
from receiver import receiver
sys.path.insert(1,'/home/pi/PiCar_ENLACE/tracker_tflite')
from tracker_complete import main as tracker
sys.path.insert(2,'/home/pi/PiCar_ENLACE/Radar_Sensor')
from heart_breath import main as heartbeat
import threading
import requests

def heart_breath_sensor():
    heartbeat()

if __name__=="__main__":
    try:
        #start receiving sensor data
        receiver()
        #continues when receiver loop breaks
        print("\nSensor Activated: Start Tracker")
        #start heart/breath rate detector thread
        HRsensor = threading.Thread(target=heart_breath_sensor,daemon=True)
        HRsensor.start()
        #start tracker
        tracker()
        
    except KeyboardInterrupt:
        print("end")