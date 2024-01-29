import torch
import numpy as np
import cv2

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
# model.conf = 0.5    #精度限制
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW) #更改API設置加上,cv2.CAP_DSHOW

while cap.isOpened():
    success, frame = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue
    frame = cv2.resize(frame,(800,480))
    results = model(frame)
    print(np.array(results.render()).shape)
    cv2.imshow('YOLO COCO 01', np.squeeze(results.render()))
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()

