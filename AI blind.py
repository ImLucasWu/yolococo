# detect03.py
import torch
import numpy as np
import cv2
import pyttsx3
import time

model = torch.hub.load('ultralytics/yolov5', 'custom',
                       path='yolov5/runs/train/exp14/weights/best.pt',force_reload=True) #exp 6 為導盲杖辨識訓練模型
# model.conf = 0.6    #精度限制
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)#更改API設置加上,cv2.CAP_DSHOW
# cap = cv2.VideoCapture("C:/Users/user/Desktop/吳紳文/stairtest01.mp4")
#cap = cv2.VideoCapture("C:/Users/user/Desktop/吳紳文/導盲杖影片/obstacle02.mp4") #(holo13 & exp15)

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
            label_index = int(d[-1])  # 目標類別的索引
            label = model.names[label_index]  # 目標的名稱
            if label == 'person':
                #print(f'Detected: {label} - 前方有人')
                print(f'{label}')
                print('前方有人請小心')
                # txt = '前方有人請小心'
                # engine = pyttsx3.init()
                # engine.say(txt)
                # engine.runAndWait()
            elif label == 'stair':
                #print(f'Detected: {label} - 前方有樓梯請小心')
                print(f'{label}')
                print('前方有樓梯請小心')
                txt = '前方有樓梯請小心'
                engine = pyttsx3.init()
                engine.say(txt)
                engine.runAndWait()
            elif label == 'hole':
                #print(f'Detected: {label} - 前方有坑洞請小心')
                print(f'{label}')
                print('前方有坑洞請小心')
                # txt = '前方有坑洞請小心'
                # engine = pyttsx3.init()
                # engine.say(txt)
                # engine.runAndWait()
            elif label == 'obstacle':
                #print(f'Detected: {label} - 前方有障礙物')
                print(f'{label}')
                print('前方有障礙物')
                txt = '前方有障礙物請小心'
                engine = pyttsx3.init()
                engine.say(txt)
                engine.runAndWait()
            elif label == 'car':
                #print(f'Detected: {label} - 前方有車子')
                print(f'Detected: {label}')
                print('前方有車子')
                # txt = '前方有車子請小心'
                # engine = pyttsx3.init()
                # engine.say(txt)
                # engine.runAndWait()
            else:
                print(f'Detected: {label}')

    cv2.imshow('YOLO COCO AI blind detection', np.squeeze(results.render()))

    # time.sleep(1 / 60)  # 暫停 1/30 秒（30 幀每秒）

    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
