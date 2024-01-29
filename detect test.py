import torch
import cv2
import numpy as np
import pyttsx3
import time


model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

counter = 0  # 計數器
detection_interval = 5  # 每5秒偵測一次

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    frame = cv2.resize(frame, (800, 480))
    results = model(frame)

    det = results.pred[0]
    if det is not None and len(det):
        for d in det:
            label_index = int(d[-1])  # 目標類別的索引
            label = model.names[label_index]  # 目標的名稱
            if label == 'person':
                print(f'Detected: {label} - 前方有人請小心')
                # txt = '前方有人請小心'
                # engine = pyttsx3.init()
                # engine.say(txt)
                # engine.runAndWait()
            elif label == 'cell phone':
                print(f'Detected: {label} - 不要玩手機')
            else:
                print(f'Detected: {label}')

    cv2.imshow('YOLO COCO 01', np.squeeze(results.render()))

    counter = (counter + 1) % (detection_interval * 60)  # 計數器每次加1，並取模以確保在一定時間後歸零

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
