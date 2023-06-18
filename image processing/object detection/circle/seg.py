import cv2

# Load the image
img = cv2.imread('picture/FRAME38.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply thresholding to the image
_, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

# Find contours in the image
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Filter the contours based on their size
filtered_contours = []
for cnt in contours:
    if cv2.contourArea(cnt) > 1000:
        filtered_contours.append(cnt)

# Draw the filtered contours on the image
cv2.drawContours(img, filtered_contours, -1, (0, 255, 0), 3)

# Display the image
cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()