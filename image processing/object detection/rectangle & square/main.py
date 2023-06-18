# rectangle object dection code

# import libary
import numpy as np
import cv2 as cv

# image read
img2 = cv.imread('picture/51c.jpg')
shape=img2.shape[:2]
print(shape)
# object detection
imgray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
ret,edge = cv.threshold(imgray,220,255,cv.THRESH_BINARY_INV)

# object location
contours, hierarchy = cv.findContours(edge, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

# identifying the maxmium values to remove noise
maxlen=len(contours[0])
index=0
for cnt in range(len(contours)):
    v=len(contours[cnt])
    if maxlen<v:
        maxlen=v
        index=cnt

# location points
approx = cv.approxPolyDP(contours[index], 0.01*cv.arcLength(contours[index], True), True)
print(len(approx))
if len(approx) == 10:

    x,y,w,h=cv.boundingRect(contours[index])
    length=(x+w)-x
    width=(y+h)-y
   
    print(length,width)
    aspect_ratio = float(w) / float(h)
    area=cv.contourArea(contours[index])
    print(area)
    M = cv.moments(contours[index])
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    print(cx,cy)

    if aspect_ratio >= 0.95 and aspect_ratio <= 1.05:
        print("Square")
        
        if 35000<area>40000 or length*width==38009: 
            new_frame=cv.rectangle(img2,(x,y),(x+w,y+h),(0,0,255),1)
            new_image=img2[y:y+h+1,x:x+w+1]

        else:
            print("OBJECT IS  BREAK")

    else:
        print("Rectangle")

        if area<40000: 
            new_frame=cv.rectangle(img2,(x,y),(x+w,y+h),(0,0,255),1)
            new_image=img2[y:y+h+1,x:x+w+1]
            hsv = cv.cvtColor(new_image, cv.COLOR_BGR2HSV)
            lower = np.array([15, 50, 0])
            upper = np.array([170, 255, 255])
            mask = cv.inRange(hsv, lower, upper)
            result = cv.bitwise_and(new_image, new_image, mask=mask)
 
        else:
            print("OBJECT IS  BREAK")

else:
    print("circle")
    



cv.imshow('frame1',img2)

cv.imshow('frame6',imgray)

cv.imshow('frame2',edge)

cv.imshow('frame5',new_image)

cv.imshow('frame3',hsv) 

cv.imshow('frame4',result)




cv.waitKey(0)

cv.destroyAllWindows()
