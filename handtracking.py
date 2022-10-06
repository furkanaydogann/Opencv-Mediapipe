import cv2
import time
import mediapipe as mp

cap = cv2.VideoCapture(0)
mpHand = mp.solutions.hands
hands = mpHand.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0
while True:
    seccess, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHand.HAND_CONNECTIONS)
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                
                if id  == 12:
                    cv2.circle(img, (cx,cy), 6, (255,0,0), cv2.FILLED)
                    cv2.putText(img, "ff", (cx,cy), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255))
                
    #FPS
    cTime = time.time()
    fps = 1/ (cTime - pTime)
    pTime = cTime                                            
    cv2.putText(img,"FPS: " + str(int(fps)), (10,75), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 5)
        
    cv2.imshow("Live Camm", img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        break



