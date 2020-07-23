import cv2
import keyboard
import numpy
import time

fps = 30
wait = 33.33

def updtFps(fps):
    if(fps < 0)
     fps = 1
    wait = int((1/fps)*1000.00)

def empty(a):
    pass

def getBase(): 
    cam = cv2.VideoCapture(0)

    while True:
        ret,current = cam.read()
        cv2.imshow("RESULT",current)
        if cv2.waitKey(wait) & 0xFF == ord('s'):
                base = current.copy()
                cam.release()
                cv2.destroyAllWindows()
                return base

def colorPicker(): 
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("OPTIONS")
    cv2.resizeWindow("OPTIONS",640,290)
    
    cv2.createTrackbar("Hue <","OPTIONS",0,179,empty)
    cv2.createTrackbar("Hue >","OPTIONS",179,179,empty)
    cv2.createTrackbar("Sat <","OPTIONS",0,255,empty)
    cv2.createTrackbar("Sat >","OPTIONS",255,255,empty)
    cv2.createTrackbar("Val <","OPTIONS",0,255,empty)
    cv2.createTrackbar("Val >","OPTIONS",255,255,empty)
    
    while True:
        ret,current = cam.read()
        if ret:
            HSVimg = cv2.cvtColor(current,cv2.COLOR_BGR2HSV)
            hmin = cv2.getTrackbarPos("Hue <","OPTIONS")
            hmax = cv2.getTrackbarPos("Hue >","OPTIONS")
            smin = cv2.getTrackbarPos("Sat <","OPTIONS")
            smax = cv2.getTrackbarPos("Sat >","OPTIONS")
            vmin = cv2.getTrackbarPos("Val <","OPTIONS")
            vmax = cv2.getTrackbarPos("Val >","OPTIONS")
        
            lower = numpy.array([hmin,smin,vmin])
            upper = numpy.array([hmax,smax,vmax])
            mask = cv2.inRange(HSVimg,lower,upper)
    
            result = cv2.bitwise_and(current,current,mask=mask)
            cv2.imshow("RESULT",result)
            
            if cv2.waitKey(wait) & 0xFF == ord('s'):
                cam.release()
                cv2.destroyAllWindows()
                return lower,upper


def main():
    base = getBase()
    lower,upper=colorPicker()
    cv2.namedWindow("options")
    cv2.resizeWindow("options",480,100)
    cv2.createTrackbar("fps","options",0,500,updtFps)

    cap = cv2.VideoCapture(0)
    while True:
        ret,frame = cap.read() 
        if ret:
            HSVimg = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            cloak = cv2.inRange(HSVimg,lower,upper)

            #Refine the cloak
            cloak = cv2.morphologyEx(cloak,cv2.MORPH_OPEN,numpy.ones((3,3),numpy.uint8),iterations=2)
            cloak = cv2.morphologyEx(cloak,cv2.MORPH_DILATE,numpy.ones((3,3),numpy.uint8),iterations=1)
            invertedCloak = cv2.bitwise_not(cloak)
            
            #get background and foreground
            back = cv2.bitwise_and(base,base,mask=cloak)
            fore = cv2.bitwise_and(frame,frame,mask=invertedCloak)

            #calculate result by adding foreground with background
            result = cv2.addWeighted(back,1,fore,1,0)
            cv2.imshow("RESULT",result)

        if cv2.waitKey(wait) and 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break 
   

if __name__ == '__main__':
    main()
