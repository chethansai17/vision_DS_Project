# In this python file the frame get read and saved in the video form.

# importing libraries
import numpy as np
import cv2 as cv
import math

# Create a VideoCapture object and read from input file
cap = cv.VideoCapture(0)
fourcc=cv.VideoWriter_fourcc(*'DIVX') 
out = cv.VideoWriter('project.avi', fourcc, 1, (640, 480))

# Check if camera opened successfully
if (cap.isOpened()== False):
	print("Error opening video file")

# input parameters

# rectangle
Length_rectangle=203 # length
width_rectangle=293  # width
rectangle_range1,rectangle_range2=40000,50000  # area of rectangle varies

# square
square_range1,square_range2=35000,40000
size=160

# circle
circles_area1,circles_area2=0,0
major_radius=0
minor_radius=0

# Read until video is completed
while(cap.isOpened()):
	
# Capture frame-by-frame
	ret, frame = cap.read()
	if ret == True:

        # save the frame
		out.write(frame)
		shape=frame.shape[:2]
		
        # object detection
		imgray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
		ret,treshold = cv.threshold(imgray,215,510,cv.THRESH_BINARY)
		
        # object location
		contours, hierarchy = cv.findContours(treshold, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
		
        # identifying the maxmium values to remove noise
		maxlen=len(contours[0])
		index=0
		for cnt in range(len(contours)):
			v=len(contours[cnt])
			if maxlen<v:
				maxlen=v
				index=cnt
				
		main_zone=contours[index]		
		approx = cv.approxPolyDP(main_zone, 0.01*cv.arcLength(contours[index], True), True)
		
        # rectangle & square
		if len(approx) == 4:
			
			x,y,w,h=cv.boundingRect(main_zone) # collecting positions
			
			length=(x+w)-x
			width=(y+h)-y
			aspect_ratio = float(w) / float(h)
			area=cv.contourArea(main_zone)
			
            # sqaure 
			if aspect_ratio >= 0.95 and aspect_ratio <= 1.05: # center moment is same 
				print("Square")
				
                # desire object sizes
				if rectangle_range1<area>rectangle_range2 and length==Length_rectangle and width==width_rectangle: 
					
					new_frame=cv.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),1)
					new_image=frame[y:y+h+1,x:x+w+1] # new image after segmentation
					
				else:
					print("OBJECT IS  BREAK")
					continue

            # rectangle		
			else:
				print("Rectangle")
			
				if square_range1<area>square_range1 and length==size==width: # checking for dimension satisfaction
					
					new_frame=cv.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),1)
					new_image=frame[y:y+h+1,x:x+w+1] # new image after segmentation
					
				else:
					print("OBJECT IS  BREAK")
					continue
					
		else:
			if len(approx)>15:
				print("circle")
				Area_cir=cv.contourArea(main_zone)
				circles = cv.HoughCircles(imgray, cv.HOUGH_GRADIENT, 1, 200, param1=100, param2=30, minRadius=0, maxRadius=0)
				x,y,r = np.round(circles[0, :]).astype("int").flatten()
				
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
				
				cv.circle(frame,(data1[location1].flatten().tolist()),1,(0,255,0),-1)
				cv.circle(frame,(data1[location2].flatten().tolist()),1,(0,255,0),-1)
				
				# desire object sizes
				if (circles_area1<Area_cir>circles_area2) and ((maximum,minimum) in range (minor_radius,minor_radius)):
					
					# segmentation through maximum points
					leftmost=tuple(main_zone[main_zone[:,:,0].argmin()][0])
					rightmost=tuple(main_zone[main_zone[:,:,0].argmax()][0])
					topmost=tuple(main_zone[main_zone[:,:,1].argmin()][0])
					bottommost=tuple(main_zone[main_zone[:,:,1].argmax()][0])
					
                    # new image after segmentation
					new_image=frame[topmost[1]:bottommost[1],leftmost[0]:rightmost[0]] 
				
				else:
					print("OBject break")
					continue
		
        # background subtraction


        # Display the resulting frame
		cv.imshow('Frame', frame)
		cv.imshow("B & W", imgray)
		cv.imshow('detection',treshold)
		cv.imshow('new image', new_image)
		
	# Press Q on keyboard to exit
		if cv.waitKey(25) & 0xFF == ord('q'):
			break

# Break the loop
	else:
		print("Capture of image get stoped")
		break

# stoping the video
cap.release()

# Closes all the frames
cv.destroyAllWindows()