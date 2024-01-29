from mpu6050 import mpu6050
import RPi.GPIO as GPIO
import time
import torch
import numpy as np
import cv2
import pyttsx3

# 初始化MPU6050
address = 0x68
sensor = mpu6050(address)

# 初始化蜂鳴器GPIO
buzzer_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)

# 初始化超聲波感測器的GPIO引腳
TRIG = 23
ECHO = 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# 初始化YOLO模型
model = torch.hub.load('ultralytics/yolov5', 'custom',
                       path='yolov5/runs/train/exp14/weights/best.pt', force_reload=True)


# 蜂鳴器警報函數
def activate_alarm():
    GPIO.output(buzzer_pin, GPIO.HIGH)
    print("警報器已啟動")


def deactivate_alarm():
    GPIO.output(buzzer_pin, GPIO.LOW)
    print("警報器已停止")


# 超聲波感測函數
def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.1)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance


# 導盲杖是否倒下函數
def cane_dropped():
    data = sensor.get_accel_data()
    y_acc = data['y']
    if y_acc < -8:
        return True
    return False


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    frame = cv2.resize(frame, (800, 480))

    # YOLO影像辨識
    results = model(frame)
    det = results.pred[0]

    # 處理YOLO結果
    if det is not None and len(det):
        for d in det:
            label_index = int(d[-1])
            label = model.names[label_index]
            if label in ['person', 'stair', 'hole', 'obstacle', 'car']:
                print(f'Detected: {label}')
                activate_alarm()
                txt = f'前方有{label}，請小心'
                engine = pyttsx3.init()
                engine.say(txt)
                engine.runAndWait()

    # 處理導盲杖倒下事件
    if cane_dropped():
        activate_alarm()
        print("拐杖掉落")
        while True:
            data = sensor.get_accel_data()
            y_acc = data['y']
            if y_acc > -6:
                break
            time.sleep(0.1)
        deactivate_alarm()

    # 超聲波感測距離
    distance = get_distance()
    print("距離：", distance, "公分")

    # 根據距離啟動蜂鳴器
    if distance <= 200 and distance > 100:
        activate_alarm()
    elif distance <= 100:
        activate_alarm()
        while distance <= 100:
            activate_alarm()
            distance = get_distance()
            time.sleep(0.1)
            time.sleep(0.1)
            deactivate_alarm()
            time.sleep(0.1)
    else:
        deactivate_alarm()

    cv2.imshow('YOLO COCO AI blind detection', np.squeeze(results.render()))

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
