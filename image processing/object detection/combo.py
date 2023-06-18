import numpy as np
import cv2 


img = cv2.imread('Screenshot 2023-04-07 061226.png')


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply thresholding
_, thresh = cv2.threshold(gray, 235, 255, cv2.THRESH_BINARY)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for i in contours:
    print(i)

# Draw contours
cv2.drawContours(img, contours, -1, (0,255,0), 3)

# Display image
cv2.imshow('Image', img)
cv2.imshow('Image1', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()
