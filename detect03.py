# detect03.py
import torch
import numpy as np
import cv2

model = torch.hub.load('ultralytics/yolov5', 'custom',
                       path='yolov5/runs/train/exp4/weights/best.pt',force_reload=True) #exp 4 為口罩辨識訓練模型
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)#更改API設置加上,cv2.CAP_DSHOW

while cap.isOpened():
    success, frame = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue
    frame = cv2.resize(frame,(800,480))
    results = model(frame)
    # print(np.array(results.render()).shape)

    det = results.pred[0]
    if det is not None and len(det):
        for d in det:
            label = model.names[int(d[-1])]  # 提取目標的名稱
            print(f'Detected: {label}')

    cv2.imshow('YOLO COCO 03 mask detection', np.squeeze(results.render()))
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
