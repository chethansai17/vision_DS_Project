import numpy as np
import cv2 as cv
import math
import time

new = cv.imread('picture/win.jpg')

c=new.shape[:2]

imgray1= cv.cvtColor(new, cv.COLOR_BGR2GRAY)


ret,edge = cv.threshold(imgray1,215,255,cv.THRESH_BINARY)
kernel = np.ones((5,5),np.uint8)
opening = cv.morphologyEx(edge, cv.MORPH_OPEN, kernel)
opening = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel)

cv.imshow("frame1",opening)
contours, hierarchy = cv.findContours(opening, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)


list2=[]
for i in contours:
    x,y,w,h=cv.boundingRect(i)
    if len(i) in range(300,500):
        list1=[x,y,w,h]
        list2.append(list1)

for j in list2:
    # new_image=img2[y:y+h+1,x:x+w+1]
    img2=new[j[1]-4:j[1]+j[3]+5,j[0]-4:j[0]+j[2]+5]
    
    imgray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
    cv.imshow("frame2",imgray)
    ret,edge = cv.threshold(imgray,96,205,cv.THRESH_BINARY)
    cv.imshow('Frea',edge)
# edge=cv2.Canny(img2,700,1000)
    contour, hierarchy = cv.findContours(edge, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)


    major_radius=128
    minor_radius=126

    maxlen=len(contour[0])
    index=0
    for cnt in range(len(contour)):
        v=len(contour[cnt])
        if maxlen<v:
            maxlen=v
            index=cnt

    a=contour[index]
    Area=cv.contourArea(contour[index])		
    cv.drawContours(img2,contour[index],-1,(0,0,255),1)

    M = cv.moments(contour[index])
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv.circle(img2, (cx, cy), 2, (0, 0, 255), -1)
        print(f"x: {cx} y: {cy}")


    li=[]
    d=(cx,cy)
    for i in range(0,len(a)):
        b=(a[i].flatten())
        b1=list(b.tolist())
        va=int(math.dist(d,b1))
        li.append(va)

    print(min(li),max(li))

    cv.imshow("frame",img2)
    cv.waitKey(25)
    time.sleep(8)
    
