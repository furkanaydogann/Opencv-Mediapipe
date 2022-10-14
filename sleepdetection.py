import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot

cap = cv2.VideoCapture(0)

detector = FaceMeshDetector()
plotY = LivePlot(540, 360, [10, 60])

idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243] #eye id left
color = (0, 0, 255)
ratioList = []
counter = 0
blickCounter = 0

while True:
    
    ret, frame = cap.read()
    frame, faces = detector.findFaceMesh(frame, draw = False)
    
    if faces:
        face = faces[0]
        
        for id in idList:
            cv2.circle(frame, face[id], 1, color, cv2.FILLED)
        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130] 
        leftRigth = face[243]
        
        lengthVer, _ = detector.findDistance(leftUp, leftDown)
        lengthHor, _ = detector.findDistance(leftLeft, leftRigth)
        
        cv2.line(frame, leftUp, leftDown, (0, 255, 0), 1)
        cv2.line(frame, leftLeft, leftRigth, (0, 255, 0), 1)
        ratio = int((lengthVer/lengthHor)*100)
        ratioList.append(ratio)
        
        if len(ratioList) > 3:
            ratioList.pop(0)
            
        ratioAvg = sum(ratioList)/len(ratioList)
        
        if ratioAvg < 33 and counter == 0:
            blickCounter += 1
            color = (0, 255, 0)
            counter == 1
        if counter != 0:
            counter += 1
            if counter > 10:
                counter = 0
                color = (0, 0, 255)
        cvzone.putTextRect(frame, f"BlickCount: {blickCounter}", (50, 100), colorR = color)
        imgPlot = plotY.update(ratioAvg, color)
        frame = cv2.resize(frame, (640,360))
        imgStack = cvzone.stackImages([frame, imgPlot], 2, 1)
    cv2.imshow("Live", imgStack)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        break 
    

