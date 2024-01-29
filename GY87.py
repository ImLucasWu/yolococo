#树莓派 3 和九轴传感器来检测树莓派是否倒下，并在倒下时触发蜂鸣器的Python程序


#这个程序会不断读取九轴传感器的加速度数据，并检测是否树莓派倒下（当z轴加速度小于0.5时）。如果检测到倒下，蜂鸣器将被触发。当树莓派重新竖立时，蜂鸣器将停止响声。

#请注意，此示例代码可能需要根据您的具体硬件和需求进行调整。确保您已连接九轴传感器和蜂鸣器，并已正确设置树莓派的GPIO引脚


#pip install RPi.GPIO smbus-cffi


import RPi.GPIO as GPIO
import smbus
import time

# 初始化GPIO设置
GPIO.setmode(GPIO.BCM)
buzzer_pin = 17  # 通过GPIO 17连接蜂鸣器
GPIO.setup(buzzer_pin, GPIO.OUT)

# 初始化九轴传感器
bus = smbus.SMBus(1)
address = 0x68  # MPU6050的I2C地址

# 配置MPU6050
bus.write_byte_data(address, 0x6B, 0)
time.sleep(1)

def read_acceleration():
    raw_data = bus.read_i2c_block_data(address, 0x3B, 6)
    ax = (raw_data[0] << 8 | raw_data[1]) / 16384.0
    ay = (raw_data[2] << 8 | raw_data[3]) / 16384.0
    az = (raw_data[4] << 8 | raw_data[5]) / 16384.0
    return ax, ay, az

try:
    while True:
        ax, ay, az = read_acceleration()
        # 检测倒下
        if az < 0.5:
            GPIO.output(buzzer_pin, GPIO.HIGH)  # 触发蜂鸣器
        else:
            GPIO.output(buzzer_pin, GPIO.LOW)  # 停止蜂鸣器
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()


