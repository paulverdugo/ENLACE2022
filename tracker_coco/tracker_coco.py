import cv2
from Imports.camera import Camera

cam = Camera()
cam.to_position(90,130)

thres = 0.55 # Threshold to detect object

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

def getObjects(img, thres, nms, draw=True, objects=[]):
    xC=0
    yC=0
    height=0
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            max_score=max(confs.flatten())
            if className in objects and confidence==max_score: #print most probable to be person
                objectInfo.append([box,className])
                if (draw):
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

    return img,objectInfo

if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    cap.set(3,360) #640 # -10 deviation with 360 (350)
    cap.set(4,270) #480 # +18 deviation with 270 (288)
    #cap.set(10,70)
    
    while True:
        success, img = cap.read()
        result, objectInfo = getObjects(img,0.45,0.2, objects=['person'])
        cv2.circle(img,(0,0),2,color=(0,0,255),thickness=5)
        print(objectInfo)
        cv2.imshow("Output",img)
        cv2.waitKey(1)
