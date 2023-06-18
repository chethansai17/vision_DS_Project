import numpy as np
import cv2 as cv
import math
import time


img2 = cv.imread('picture/break.jpg')
imgray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
ret,edge = cv.threshold(imgray,215,510,cv.THRESH_BINARY_INV)
# edge=cv2.Canny(img2,700,1000)
contour, hierarchy = cv.findContours(edge, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)


major_radius=40
minor_radius=80

maxlen=len(contour[0])
index=0
for cnt in range(len(contour)):
    v=len(contour[cnt])
    if maxlen<v:
        maxlen=v
        index=cnt

main_zone=contour[index]
Area=cv.contourArea(contour[index])	
print(Area)	

cv.drawContours(img2,contour[index],-1,(0,0,255),1)

M = cv.moments(contour[index])
if M['m00'] != 0:
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cv.circle(img2, (cx, cy), 2, (0, 0, 255), -1)
    print(f"x: {cx} y: {cy}")

li=[]
a=contour[index]
d=(cx,cy)
for i in range(0,len(a)):
    b=(a[i].flatten())
    b1=list(b.tolist())
    va=int(math.dist(d,b1))
    li.append(va)

print(min(li),max(li))
ni=li.index(min(li))
le=li.index(max(li))
cv.circle(img2,(a[ni].flatten().tolist()),1,(0,255,0),-1)
cv.circle(img2,(a[le].flatten().tolist()),1,(0,255,0),-1) 

				
# desire object sizes
if (ni,le in range(minor_radius,major_radius) ):
    leftmost=tuple(main_zone[main_zone[:,:,0].argmin()][0])
    rightmost=tuple(main_zone[main_zone[:,:,0].argmax()][0])
    topmost=tuple(main_zone[main_zone[:,:,1].argmin()][0])
    bottommost=tuple(main_zone[main_zone[:,:,1].argmax()][0])
    new_image=img2[topmost[1]:bottommost[1],leftmost[0]:rightmost[0]]

else:
    print("break")

cv.imshow('frame1',img2)

cv.imshow('frame2',edge)

cv.imshow('frame3',new_image)



cv.waitKey(0)

cv.destroyAllWindows()