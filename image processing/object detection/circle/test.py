import numpy as np
import cv2 as cv
import math
import time


img2 = cv.imread('picture/circular - Copy.png',)
imgray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
ret,edge = cv.threshold(imgray,215,510,cv.THRESH_BINARY_INV)
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

main_zone=contour[index]
circles = cv.HoughCircles(imgray, cv.HOUGH_GRADIENT, 1, 200, param1=100, param2=30, minRadius=0, maxRadius=0)
dimension=circles.flatten()
x=int(dimension[0])
y=int(dimension[1])
r=int(dimension[2])
cv.circle(img2,(x,y),r,(0,255,0),1)				
# detemine major and minor diameter
	
data1=[]
for i in range(0,len(main_zone)):
	b=(main_zone[i].flatten())
	b1=list(b.tolist())
	va=int(math.dist((x,y),b1))
	data1.append(va)
					
minimum=min(data1) 
maximum=max(data1) 
				
location1=data1.index(minimum)
location2=data1.index(maximum)
				
# cv.circle(img2,(main_zone[location1].flatten().tolist()),4,(0,255,0),-1)
# cv.circle(img2,(main_zone[location2].flatten().tolist()),4,(0,255,0),-1)
				
# desire object sizes
if (minimum,maximum in range(minor_radius,major_radius) ):
    leftmost=tuple(main_zone[main_zone[:,:,0].argmin()][0])
    rightmost=tuple(main_zone[main_zone[:,:,0].argmax()][0])
    topmost=tuple(main_zone[main_zone[:,:,1].argmin()][0])
    bottommost=tuple(main_zone[main_zone[:,:,1].argmax()][0])
    new_image=img2[topmost[1]:bottommost[1],leftmost[0]:rightmost[0]]

    ret,tresh = cv.threshold(new_image,215,510,cv.THRESH_BINARY_INV)

    list2=[]
    a=0
    b=0

    test=np.array([255,255,255])
    test1=np.array([0,255,0])
    shape=new_image.shape[:2]
    let=int(shape[1]/2)
    for i in range(0,shape[1]):
        for j in range(0,shape[0]):
            compare1=new_image[i][j]
            new1=np.array_equal(test,compare1)
            new2=np.array_equal(test1,compare1)
            if a==0 and new1== True:
                new_image[i][j]=np.array([0,0,0])
            elif a==0 and new2==True :
                a=1
            elif a==1 and new1==True:
                continue
            elif a==1 and new2==True:
                a=0
        a=0

cv.imshow('frame1',img2)

cv.imshow('frame2',edge)

cv.imshow('frame3',new_image)



cv.waitKey(0)

cv.destroyAllWindows()