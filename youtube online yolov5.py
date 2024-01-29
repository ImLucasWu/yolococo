import torch
import numpy as np
import cv2
import time
import pafy


prev_time = 0 #加上FPS
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model.conf = 0.5

# url = "https://www.youtube.com/watch?v=eIX9IyYG0f4"
url = "https://www.youtube.com/watch?v=uqcz-xfs54o"
live = pafy.new(url)
stream = live.getbest(preftype="mp4")

cap = cv2.VideoCapture(stream.url)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue
    frame = cv2.resize(frame,(960,540))
    results = model(frame)
    output_image = np.squeeze(results.render())
    cv2.putText(output_image, f'FPS: {int(1 / (time.time() - prev_time))}',
                (3, 40), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
    prev_time = time.time()
    cv2.imshow('Doggy youtube online', output_image)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()