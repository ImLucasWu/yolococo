import torch
import numpy as np
import cv2
import pyttsx3

model = torch.hub.load('ultralytics/yolov5', 'custom',
                       path='yolov5/runs/train/exp14/weights/best.pt', force_reload=True)

# model.conf = 0.6    #精度限制
# cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)#更改API設置加上,cv2.CAP_DSHOW
cap = cv2.VideoCapture("C:/Users/user/Desktop/吳紳文/導盲杖影片/stairtest01.mp4")

frame_count = 0  # 初始化幀計數器

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    frame = cv2.resize(frame, (800, 480))

    if frame_count % 30 == 0:  # 每30幀進行辨識
        results = model(frame)

        det = results.pred[0]
        if det is not None and len(det):
            for d in det:
                label_index = int(d[-1])
                label = model.names[label_index]

                # 處理偵測結果
                if label == 'person':
                    # print(f'Detected: {label} - 前方有人')
                    print(f'{label}')
                    print('前方有人請小心')
                    # txt = '前方有人請小心'
                    # engine = pyttsx3.init()
                    # engine.say(txt)
                    # engine.runAndWait()
                elif label == 'stair':
                    # print(f'Detected: {label} - 前方有樓梯請小心')
                    print(f'{label}')
                    print('前方有樓梯請小心')
                    txt = '前方有樓梯請小心'
                    engine = pyttsx3.init()
                    engine.say(txt)
                    engine.runAndWait()
                elif label == 'hole':
                    # print(f'Detected: {label} - 前方有坑洞請小心')
                    print(f'{label}')
                    print('前方有坑洞請小心')
                    # txt = '前方有坑洞請小心'
                    # engine = pyttsx3.init()
                    # engine.say(txt)
                    # engine.runAndWait()
                elif label == 'obstacle':
                    # print(f'Detected: {label} - 前方有障礙物')
                    print(f'{label}')
                    print('前方有障礙物')
                    txt = '前方有障礙物請小心'
                    engine = pyttsx3.init()
                    engine.say(txt)
                    engine.runAndWait()
                elif label == 'car':
                    # print(f'Detected: {label} - 前方有車子')
                    print(f'Detected: {label}')
                    print('前方有車子')
                    # txt = '前方有車子請小心'
                    # engine = pyttsx3.init()
                    # engine.say(txt)
                    # engine.runAndWait()
                else:
                    print(f'Detected: {label}')

        cv2.imshow('YOLO COCO AI blind detection', np.squeeze(results.render()))

    frame_count += 1

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
