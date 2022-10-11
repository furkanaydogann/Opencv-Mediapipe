import cv2
import pickle
import numpy as np


def checkParkSpace(imgg):
    spaceCounter = 0
    
    for pos in posList:
        x, y = pos
        img_crop = imgg[y: y + height, x: x +width]
        count = cv2.countNonZero(img_crop)
        print(count)
        
        if count < 150:
            color = (0,  255, 0)
            spaceCounter += 1
        else:
            color = (0, 0, 255)
        
        cv2.rectangle(frame, pos, (pos[0] + width, pos[1] + height), color, 2)
    cv2.putText(frame, f"Bos: {spaceCounter} / {len(posList)}", (15, 25), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
    
width = 27
height = 15

cap = cv2.VideoCapture("video.mp4")

with open("CarParkPose", "rb") as f:
    posList = pickle.load(f)
    

while True:
    ret, frame = cap.read()
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(frameGray, (3,3), 1) #detayları yok ettik
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    imgDilate = cv2.dilate(imgMedian, np.ones((3,3)), iterations = 1)
    
    checkParkSpace(imgDilate)
    
    
    
    
    
    
    cv2.imshow("otopark", frame)
    k = cv2.waitKey(50) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        break 
    