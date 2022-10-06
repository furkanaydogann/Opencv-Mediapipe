import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)


mpHand = mp.solutions.hands
hands = mpHand.Hands()
mpDraw = mp.solutions.drawing_utils
tipIds = [4, 8, 12, 16, 20]
while True:
    succes, image = cap.read()
    imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results =hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    
    lmList = []
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(image, handLms, mpHand.HAND_CONNECTIONS)
            
            for id, lm in enumerate(handLms.landmark):
                h, w, _ = image.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
                #işaret uç noktası
                #if id == 8:
                #    cv2.circle(image, (cx, cy), 9, (255,0,0), cv2.FILLED)
                #işaret uç noktası
                #if id == 6:
                #    cv2.circle(image, (cx, cy), 9, (0,0,255), cv2.FILLED)
    if len(lmList) != 0: 
        fingers = []
        # basparmak
        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        #4 parmak
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        #print(fingers)
        totalF = fingers.count(1)
        #print(totalF)
        cv2.putText(image, str(totalF), (30,125), cv2.FONT_HERSHEY_PLAIN, 8, (0,0,255), 7)
                
                    
            
    cv2.imshow("Live", image)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        break