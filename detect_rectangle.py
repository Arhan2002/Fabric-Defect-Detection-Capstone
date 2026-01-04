import cv2
import numpy as np


def is_valid_rectangle(rectangle, min_diagonal_length, frame, corner_margin=10):
    x, y, w, h = cv2.boundingRect(rectangle)
    if x <= corner_margin or y <= corner_margin or x + w >= frame.shape[1] - corner_margin or y + h >= frame.shape[
        0] - corner_margin:
        return False
    diagonal_length = np.sqrt(w ** 2 + h ** 2)
    return diagonal_length >= min_diagonal_length


# Define a function to check if a rectangle is not in the corners
def not_in_corners(rectangle, image, corner_margin=10):
    x, y, w, h = cv2.boundingRect(rectangle)
    return x > corner_margin and y > corner_margin and x + w < image.shape[1] - corner_margin and y + h < image.shape[
        0] - corner_margin


# Load the image
def detect_rectangle(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blurring to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny edge detection
    edges = cv2.Canny(blurred, 50, 150, apertureSize=3)

    # Find contours in the edged image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through the detected contours
    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Check if the polygon has 4 vertices, indicating a potential rectangle
        if len(approx) == 4:
            # Check if the rectangle is not in the corners
            if is_valid_rectangle(approx, 200, image):
                # Draw the rectangle
                cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
                x, y, w, h = cv2.boundingRect(approx)
                # Crop the rectangle from the original image
                cropped_rectangle = image[y:y + h, x:x + w]

                return cropped_rectangle
    # Display the marked image


if __name__ == '__main__':
    image = cv2.imread('cropped_rectangle.jpg')
    cropped_rectangle = detect_rectangle(image)
    cv2.imshow('frame', cropped_rectangle)
    cv2.waitKey(0)
