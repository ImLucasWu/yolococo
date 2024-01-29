#拍照程式
import cv2
from time import strftime
import os
#labels = ['nomask','mask']  # 0 nomask 1 mask
labels = ['Mask','NoMask']
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)


while cap.isOpened():
    success, frame = cap.read()
    cv2.imshow('get pic', frame)

    keyb = cv2.waitKey(100) & 0xFF
    if keyb == 27:
        break
    elif keyb == ord('0') or keyb == ord('1'):  #按0跟按1拍照
        print(keyb - 48)
        systime = strftime("%H%M%S") # 年月日時分秒  %Y%m%d%H%M%S
        imgname = os.path.join('images/', labels[keyb - 48] + '.' + systime + '.jpg')
        cv2.imwrite(imgname, frame)
cap.release()
cv2.destroyAllWindows()