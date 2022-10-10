import cv2
import mediapipe as mp
import numpy as np
import math



def findAngle(frame, p1, p2, p3, lmList, draw = True):
    x1, y1 = lmList[p1][1:] # p1 noktasının x, y
    x2, y2 = lmList[p2][1:] # p2 noktasının x, y
    x3, y3 = lmList[p3][1:]#zxy # p3 noktasının x, y
    
    #açı hesaplama
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    if angle < 0: angle += 360
    
    if draw:
        cv2.line(frame, (x1, y1), (x2, y2), (0,0,255),3)
        cv2.line(frame, (x3, y3), (x2, y2), (0,0,255),3)
        
        cv2.circle(frame, (x1, y1), 10, (0,255,255), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 10, (0,255,255), cv2.FILLED)
        cv2.circle(frame, (x3, y3), 10, (0,255,255), cv2.FILLED)
        
        cv2.circle(frame, (x1, y1), 15, (0,255,255))
        cv2.circle(frame, (x2, y2), 15, (0,255,255))
        cv2.circle(frame, (x3, y3), 15, (0,255,255))
        
        cv2.putText(frame, str(int(angle)), (x2 - 40, y2 + 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
    return angle




cap = cv2.VideoCapture(0)
    
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils 
dir = 0
count = 0
while True:
    ret, frame = cap.read()
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frameRGB)
    lmList = []
    if results.pose_landmarks:
        mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
    
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, _ = frame.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            lmList.append([id, cx, cy])
    
    if len(lmList) != 0:
        #şınav
        #angle = findAngle(frame, 11, 13, 15, lmList)
        #per = np.interp(angle, (185, 245), (0, 100))
        #DİZ ÇEKME
        angle = findAngle(frame, 23, 25, 27, lmList)
        per = np.interp(angle, (65, 145), (0, 100))
        if per == 100:
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            if dir == 1:
                count += 0.5
                dir = 0
        cv2.putText(frame, str(int(count)), (45, 125), cv2.FONT_HERSHEY_PLAIN, 10, (255,0,0), 10)
        
        

    cv2.imshow("Live Camm", frame)
    cv2.waitKey(25)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        break
