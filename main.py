import datetime
import time
import requests
import cv2

from detect_fabric import detect_fabric_defect
from detect_rectangle import detect_rectangle


# Initialize video capture from a camera or video file
cap = cv2.VideoCapture(0)
bad_count=0
while True:
    # Read a frame from the video
    ret, frame = cap.read()
    if not ret:
        break
    org_frame = frame
    rectangle_frame = detect_rectangle(frame)
    if rectangle_frame is None:
        cv2.imshow('Marked Image', org_frame)
        cv2.waitKey(1)
        continue

    cv2.imshow('Rectangle Image', rectangle_frame)

    h, w, _ = rectangle_frame.shape
    x = 20
    if h > x * 2 and w > x * 2:
        quality, defected_frame = detect_fabric_defect(rectangle_frame[x: h - x, x: w - x])
        print(datetime.datetime.now(), quality)
        if quality == "bad":
            bad_count+=1
            cv2.imshow('Defected Fabric', defected_frame)
        else:
            bad_count=0
        if bad_count==5:
            bad_count=0
            requests.get('https://codingprojects.cloud/set_values.php?id=16&field1=1')
            print("send cmd to stop")
            time.sleep(10)
    # Press 'q' to exit the video
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
