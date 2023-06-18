# rectangle object dection code

# import libary
import numpy as np
import cv2 as cv

# image read
img2 = cv.imread('picture/complete boiled.jpg',-1)
shape=img2.shape[:2]

# object detection
imgray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
ret,edge = cv.threshold(imgray,215,510,cv.THRESH_BINARY)

# object location
contours, hierarchy = cv.findContours(edge, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
for cnt in contours:
    print(len(cnt))
# identifying the maxmium values to remove noise
maxlen=len(contours[0])
index=0
for cnt in range(len(contours)):
    v=len(contours[cnt])
    if maxlen<v:
        maxlen=v
        index=cnt

approx = cv.approxPolyDP(contours[1], 0.01*cv.arcLength(contours[index], True), True)

if len(approx) == 7:
    
    x,y,w,h=cv.boundingRect(contours[1])

    length=(x+w)-x
    width=(y+h)-y
   
    aspect_ratio = float(w) / float(h)
    area=cv.contourArea(contours[1])

    if aspect_ratio >= 0.95 and aspect_ratio <= 1.05:
        print("Square")
        
        if 35000<area>40000 and length==width==269: 
            new_frame=cv.rectangle(img2,(x,y),(x+w,y+h),(0,255,0),1)
            new_image=img2[y:y+h+1,x:x+w+1]

        else:
            print("OBJECT IS  BREAK")

    else:
        print("Rectangle")

        if (area in range(40000,50000)) and length==171 and width==271:
            new_frame=cv.rectangle(img2,(x,y),(x+w,y+h),(0,255,0),1)
            new_image=img2[y:y+h+1,x:x+w+1]
            a=0
            test=np.array([255,255,255])
            test1=np.array([0,255,0])
            shape=new_image.shape[:2]
            let=int(shape[1]/2)
            for i in range(0,shape[0]):
                for j in range(0,shape[1]):
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

        else:
            print("OBJECT IS  BREAK")
else:
    print("circle") 
 



cv.imshow('frame1',img2)

cv.imshow('frame2',edge)

cv.imshow('frame4',new_image)



cv.waitKey(0)

cv.destroyAllWindows()
