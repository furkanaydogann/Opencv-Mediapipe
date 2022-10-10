import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
mpFaceDetection = mp.solutions.face_detection
faceDetection = mpFaceDetection.FaceDetection() # 0-1 arasında hassasiyet

mpDraw = mp.solutions.drawing_utils
while True:
    ret, frame = cap.read()
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(frameRGB)
    if results.detections:
        for id, detection in enumerate(results.detections):
            bboxC = detection.location_data.relative_bounding_box
            h, w, _ = frame.shape
            bbox = int(bboxC.xmin*w), int(bboxC.ymin*h), int(bboxC.width*w), int(bboxC.height*h)
            cv2.rectangle(frame, bbox, (255,0,0), 1)
            
    cv2.imshow("Live", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        break