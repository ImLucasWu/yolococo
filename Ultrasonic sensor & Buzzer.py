#pip install RPi.GPIO

import RPi.GPIO as GPIO
import time

# 設定超音波感測器和蜂鳴器的 GPIO 引腳
TRIG_PIN = 23  # GPIO23
ECHO_PIN = 24  # GPIO24
BUZZER_PIN = 18  # GPIO18

# 初始化 GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

def measure_distance():
    # 觸發超音波信號
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    # 監聽回波信號
    pulse_start = time.time()
    pulse_end = time.time()

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    # 計算距離
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

try:
    while True:
        # 測量距離
        distance = measure_distance()
        print(f"Distance: {distance} cm")

        # 如果距離小於3公尺，啟動蜂鳴器
        if distance < 300:
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
        else:
            GPIO.output(BUZZER_PIN, GPIO.LOW)

        time.sleep(1)

except KeyboardInterrupt:
    # 當程式中斷時執行清理動作
    GPIO.cleanup()
