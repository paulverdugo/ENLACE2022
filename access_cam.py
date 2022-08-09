import cv2

#start window thread
cv2.startWindowThread()
#get video from default camera
cap=cv2.VideoCapture(0)

while True:
    # read frame
    ret,frame=cap.read()
    """
    #turn to greyscale
    frame=cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    ret,frame=cv2.threshold(frame,80,255,cv2.THRESH_BINARY)
    """
    # display frame
    cv2.imshow('camera',frame)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()