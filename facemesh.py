import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpFacemesh = mp.solutions.face_mesh
faceMesh = mpFacemesh.FaceMesh()

mpDraw = mp.solutions.drawing_utils
drawSpec = mpDraw.DrawingSpec(thickness = 1, circle_radius = 1)
pTime = 0
while True:
    
    ret, frame = cap.read()
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(frameRGB)

    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(frame, faceLms, mpFacemesh.FACEMESH_TESSELATION, drawSpec, drawSpec) #FACEMESH_CONTOURS
            
            for id, lm in enumerate(faceLms.landmark):
                h, w, _ = frame.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(frame, "fps: " + str(int(fps)), (10,65), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                
        
    
    
    
    
    cv2.imshow("Livee", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        break