import numpy as np
import cv2 as cv



img2 = cv.imread('picture/circular - Copy.png',)
imgray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
ret,edge = cv.threshold(imgray,215,510,cv.THRESH_BINARY_INV)
# edge=cv2.Canny(img2,700,1000)
contours, hierarchy = cv.findContours(edge, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
maxlen=len(contours[0])
index=0
for i in range(len(contours)):
    v=len(contours[i])
    if maxlen<v:
        maxlen=v
        index=i


area = cv.contourArea(contours[1])
hull = cv.convexHull(contours[1])
hull_area = cv.contourArea(hull)
solidity = int(float(area) / hull_area)
print(solidity)
if solidity <=0.9:
    x, y, w, h = cv.boundingRect(contours[1])
    cv.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv.imshow('frame',img2)
cv.imshow('frame1',imgray) 
cv.imshow('frame2',edge) 

cv.waitKey(0)        