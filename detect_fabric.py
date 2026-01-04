import cv2
import numpy as np


def detect_fabric_defect(image):
    img = image.copy()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    v = hsv[:, :, 2]
    blr = cv2.blur(v, (15, 15))
    dst = cv2.fastNlMeansDenoising(blr, None, 10, 7, 21)
    _, binary = cv2.threshold(dst, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((5, 5), np.uint8)
    dilation = cv2.dilate(binary, kernel, iterations=1)
    if (dilation == 0).sum() > 1:
        contours, _ = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for i in contours:
            if cv2.contourArea(i) < 261121.0:
                cv2.drawContours(img, i, -1, (0, 0, 255), 3)

        return "bad", img
    return "good", None


if __name__ == '__main__':
    frame = cv2.imread("Defected image.png")
    data = detect_fabric_defect(frame)
    print(data[0])
    if data[0] == "bad":
        cv2.imshow('frame', data[-1])
        cv2.waitKey(0)
