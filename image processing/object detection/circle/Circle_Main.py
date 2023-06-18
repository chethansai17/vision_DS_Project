import numpy as np
import cv2 as cv
import math


img2 = cv.imread('picture/break.jpg')

c=img2.shape[:2]
imgray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
ret,edge = cv.threshold(imgray,215,255,cv.THRESH_BINARY_INV)

kernel = np.ones((5,5),np.uint8)
edge = cv.morphologyEx(edge, cv.MORPH_OPEN, kernel)
# edge=cv2.Canny(img2,700,1000)
contour, hierarchy = cv.findContours(edge, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

maxlen=len(contour[0])
index=0
for cnt in range(len(contour)):
    v=len(contour[cnt])
    if maxlen<v:
        maxlen=v
        index=cnt


approx = cv.approxPolyDP(contour[index], 0.01*cv.arcLength(contour[index], True), True)
Area=cv.contourArea(contour[index])
diameter=np.sqrt(4*Area/np.pi)
cv.drawContours
print(Area,diameter)

M = cv.moments(contour[index])
if M['m00'] != 0:
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cv.circle(img2, (cx, cy), 4, (0, 0, 255), -1)
    print(f"x: {cx} y: {cy}")

li=[]
a=contour[index]
d=(cx,cy)
for i in range(0,len(a)):
    b=(a[i].flatten())
    b1=list(b.tolist())
    va=int(math.dist(d,b1))
    li.append(va)

minimum=min(li)
maximum=max(li)
print(maximum, minimum)
ni=li.index(min(li))
le=li.index(max(li))
cv.circle(img2,(a[ni].flatten().tolist()),3,(0,255,0),-1)
cv.circle(img2,(a[le].flatten().tolist()),3,(0,255,0),-1) 

if (maximum-minimum)<=4: 
    print("Accepted")
    
else:
    print("Denine")
  


cv.imshow("frame1",img2)
cv.imshow("frame2",imgray)
cv.imshow("frame3",edge)



cv.waitKey(0)

cv.destroyAllWindows()