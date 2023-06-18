import numpy as np
import cv2 as cv

img2 = cv.imread('picture/download.jpg')
c=img2.shape[:2]
imgray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
edge = cv.adaptiveThreshold(imgray, 255, cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY_INV, 215, 3)
 

cv.imshow('frame',img2)
cv.imshow('frame1',imgray) 
cv.imshow('frame2',edge)
cv.waitKey(0) 