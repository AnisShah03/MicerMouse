import cv2 #pip install cv2
import time, numpy as np #pip install numpy
import HandTrackingModule as htm
import pyautogui #pip install pyautogui
from win32api import GetSystemMetrics
# from Speak import Speak # uncomment to import speak user-defined function 


wCam, hCam = 640, 480
cap = cv2.VideoCapture(1)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
#cTime = 0

detector = htm.handDetector(maxHands=1, detectionCon=1, trackCon=0.8)

#fingerTips
tipIds = [4, 8, 12, 16, 20]
mode = ''
active = 0   #by default off

pyautogui.FAILSAFE = False


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
   # print(lmList)
    fingers = []

    if len(lmList) != 0:

        #Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0 -1]][1]:
            if lmList[tipIds[0]][1] >= lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        elif lmList[tipIds[0]][1] < lmList[tipIds[0 -1]][1]:
            if lmList[tipIds[0]][1] <= lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)


      #  print(fingers)
        if (fingers == [0,0,0,0,0]) & (active == 0 ):
            mode='N'

        elif (fingers == [0, 1, 0, 0, 0] or fingers == [0, 1, 1, 0, 0]) & (active == 0 ):
            mode = 'Scroll'
            active = 1

        elif (fingers == [1 ,1 , 1, 1, 1] ) & (active == 0 ):
             mode = 'Cursor'
             active = 1

############# Scroll ##############

    if mode == 'Scroll':
        active = 1
     #   print(mode)
        putText(mode)
        cv2.rectangle(img, (200, 410), (245, 460), (255, 255, 255), cv2.FILLED)
        if len(lmList) != 0:
            if fingers == [0,1,0,0,0]:
              #print('up')
              #time.sleep(0.1)
                putText(mode = 'Up', loc=(200, 455), color = (0, 255, 0))
                pyautogui.scroll(300)
                # Speak('scrollimng up....') #uncomment for speak fn

            if fingers == [0,1,1,0,0]:
                #print('down')
              #  time.sleep(0.1)
                putText(mode = 'Down', loc =  (200, 455), color = (0, 0, 255))
                pyautogui.scroll(-300)
                # Speak('scrollimng down....') #uncomment for speak fn

            elif fingers == [0, 0, 0, 0, 0]:
                active = 0
                mode = 'N'

#######################################################################

    if mode == 'Cursor':
        active = 1
        #print(mode)
        putText(mode)
        cv2.rectangle(img, (110, 20), (620, 350), (255, 255, 255), 3)

        if fingers[1:] == [0,0,0,0]: #thumb excluded
            active = 0
            mode = 'N'
            print(mode)
        else:
            if len(lmList) != 0:
                x1, y1 = lmList[8][1], lmList[8][2]
                w, h =(GetSystemMetrics(0),GetSystemMetrics(1))#to get screen resolution coordinate for cursor
                X = int(np.interp(x1, [110, 620], [0, w - 1]))
                Y = int(np.interp(y1, [20, 350], [0, h - 1]))
                cv2.circle(img, (lmList[8][1], lmList[8][2]), 7, (255, 255, 255), cv2.FILLED)
                cv2.circle(img, (lmList[4][1], lmList[4][2]), 10, (0, 255, 0), cv2.FILLED)  #thumb

                if X%2 !=0:
                    X = X - X%2
                if Y%2 !=0:
                    Y = Y - Y%2

                # print(X,Y)
                # autopy.mouse.move(X,Y) autopy >>> alternate for pyautogui  #pip install autopy
                

                pyautogui.moveTo(X,Y)

                # win32api.SetCursorPos((X,Y))
                # pyautogui.moveTo(X,Y)
                
                if fingers[0] == 0:
                    cv2.circle(img, (lmList[4][1], lmList[4][2]), 10, (0, 0, 255), cv2.FILLED)  # thumb to click
                    pyautogui.click()

    cTime = time.time()
    fps = 1/((cTime + 0.01)-pTime)
    pTime = cTime

    # cv2.putText(img,f'FPS:{int(fps)}',(480,50), cv2.FONT_ITALIC,1,(255,0,0),2) #uncomment this line to show live FPS 
    cv2.imshow('Hand Tracking',img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    def putText(mode,loc = (250, 450), color = (73, 138, 242)):#color attribue >>> blue color on text
        cv2.putText(img, str(mode), loc, cv2.FONT_HERSHEY_COMPLEX_SMALL,
                    3, color, 3)





'''
1) https://www.geeksforgeeks.org/python-opencv-cv2-puttext-method/

2) Hand Tracing Module
By: Murtaza Hassan
Youtube: http://www.youtube.com/c/MurtazasWorkshopRoboticsandAI
Website: https://www.computervision.zone


'''

##################################################################################

'''
click >>> pinch thumb <<Like you do in your childhood for handgun



scorll >>> up >> use one fingers
           down >> use two fingers  
           to slow down scrolling use thum also.


NOTE :- in between scrolling first make fist after that do scrolling actions either mouse cursor action





'''