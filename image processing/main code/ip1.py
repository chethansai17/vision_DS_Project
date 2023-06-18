# In this python file the frame get read and saved in the video form as image form.

'''
spection of object contanins
        shape=Circle,rectangle, square 
	    solidity=complete solid
'''

# importing libraries
import numpy as np
import cv2 as cv
import math
import pymongo
import time

# Create a VideoCapture object and read from input file
cap = cv.VideoCapture(0)

# Check if camera opened successfully
if (cap.isOpened()== False):
	print("Error web cam is not responding")
	exit()

# input parameters

# rectangle
Length_rectangle1=108 # length
Length_rectangle2=117
width_rectangle1=177 
width_rectangle2=188 # width
rectangle_range1,rectangle_range2=10000,20000  # area of rectangle varies

# square
square_range1,square_range2=50000,60000
size=160

# circleq
circles_area1,circles_area2=50000,60000
major_radius=85
minor_radius=75

# collor detection
Colour={"Rectangle":5000,"Square":5000,"Circle":6000}
Colour1={"Rectangle":5000,"Square":5000,"Circle":6000}

# image save numbers
currentframe=0
# camera calibration

# object reach
RB_Resp_Time=2 # robot responce time in seconds
conevory_speed= 10 # Converoy speed in cm/min
conevory_dist= 60 # Distance travel

help1=1
help2=1
help4=1
# Read until video is completed
while(cap.isOpened()):
# Capture frame-by-frame
	t1=cv.getCPUTickCount()
	ret, initial = cap.read()
	if ret == True:
		initial=cv.imread("picture/14.jpg")
		initial = cv.medianBlur(initial,5)

        # object detection
		imgray = cv.cvtColor(initial, cv.COLOR_BGR2GRAY)
		ret,treshold = cv.threshold(imgray,50,253,cv.THRESH_BINARY_INV)
		cv.imshow("frame",treshold)
		cv.waitKey(0)

        # object location
		contours, hierarchy = cv.findContours(treshold, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
		
        # No object present
		if len(contours)==0:
			print("object is not found")
			continue
		
		else:
			list2=[]
			for i in contours:
				x,y,w,h=cv.boundingRect(i)
				if len(i) in range(300,600):
					M = cv.moments(i)
					if M['m00'] != 0:
						cx1 = int(M['m10']/M['m00'])
						cy1 = int(M['m01']/M['m00'])
						cv.putText(initial,str(help4),(cx1,cy1),cv.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2,cv.LINE_AA)
					list1=[x,y,w,h]
					list2.append(list1)
					help4+=1
	
			for j in list2:
				help3=str(help1)+"_"+str(help2)
				frame=initial[j[1]-1:j[1]+j[3]+1,j[0]-1:j[0]+j[2]+1]
				imgray1 = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
				ret,treshold1 = cv.threshold(imgray1,205,255,cv.THRESH_BINARY_INV)
				
                # object location
				contour1, hierarchy = cv.findContours(treshold1, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
				
                # identifying the maxmium values to remove noise
				index=0
				maxlen=len(contour1[index])
				for cnt in range(len(contour1)):
					v=len(contour1[cnt])
					if maxlen<v:
						maxlen=v
						index=cnt
						
				main_zone=contour1[0]
				approx = cv.approxPolyDP(main_zone, 0.01*cv.arcLength(main_zone, True), True)
                # rectangle & square
				if len(approx) == 8 or len(approx)==4:
					
					x1,y1,w1,h1=cv.boundingRect(main_zone) # collecting positions
					length=(x1+w1)-x1
					width=(y1+h1)-y1
					aspect_ratio = float(w1) / float(h1)
					area=cv.contourArea(main_zone)
					# cv.rectangle(frame,(x1,y1),(x1+w1,y1+h1),(0,255,0),1)
					
                    # sqaure code
					if aspect_ratio >= 0.95 and aspect_ratio <= 1.05: # center moment is same 
						test="Square"
						print(test)
						
                        # desire object sizes
						if (area in range (square_range1,square_range1)) and length==size==width : 
							test1=True
							print("No Defects")
							
						else:
							test1=False
							print("Defect")
							continue
					
                    # rectangle code
					else:
						test="Rectangle"
						print(test)
						
						if (area in range(10000,20000)) and (length in range(Length_rectangle1,Length_rectangle2)) and (width in range(width_rectangle1,width_rectangle2)): # checking for dimension satisfaction
							test1=True
							print("No Defects")
							
						else:
							test1=False
							print("Defect")
							continue

				# Circle Code
				else:
					test="Circle"
					print(test)
					Area_cir=cv.contourArea(main_zone)
				
					cv.drawContours(frame,main_zone,-1,(0,0,255),1)
					M = cv.moments(main_zone)
					if M['m00'] != 0:
						cx1 = int(M['m10']/M['m00'])
						cy1 = int(M['m01']/M['m00'])

					data1=[]
					center=(cx1,cy1)
					cv.circle(frame,center,1,(0,0,255),-1)
					for k in range(0,len(main_zone)):
						b=(main_zone[k].flatten())
						b1=list(b.tolist())
						distance=int(math.dist(center,b1))
						data1.append(distance)

					minimum=min(data1)
					maximum=max(data1)

					ni=data1.index(minimum)
					le=data1.index(maximum)
					cv.circle(frame,(main_zone[ni].flatten().tolist()),1,(0,255,0),-1)
					cv.circle(frame,(main_zone[le].flatten().tolist()),1,(0,255,0),-1) 
					
					# desire object sizes
					if (minimum-maximum)<=(major_radius-minor_radius) and (Area_cir in range(circles_area1, circles_area2)):
						test1=True
						print("No Defects")

					else:
						test1=False
						print("Defect")
						continue
					
				# color Detection
				hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
				lower = np.array([0, 70, 50])
				upper = np.array([180, 255, 255])
				mask = cv.inRange(hsv, lower, upper)
				result = cv.bitwise_and(frame, frame, mask=mask)
		
				compare1=0
				for i in result:
					a=np.array([0,0,0])
					for j in i: 
						compare=np.array_equal(a,j)
						if compare==True:
							continue
						else:
							compare1+=1   
				
				if compare1<Colour[test]:
					test2=False
					print("complete burn")

				elif compare1>Colour[test] and compare1<Colour[test]:
					test2=False
					print("half burned")

				else:
					test2=True
					print("normal")

				# Image save
				name = 'C:/storage/FRAME' + str(currentframe) + '.jpg' # frame name
				cv.imwrite(name, initial) # frame save

				# Camera Calibration

				# object Reaching time
				Rech_time=(conevory_dist/conevory_speed) - RB_Resp_Time
				print(Rech_time)
				t=time.localtime()
				current_time=time.strftime("%S",t)
				Rech_time1=Rech_time+int(current_time)


				# data storge
				client=pymongo.MongoClient("mongodb://localhost:27017")
				database=client["Project"]
				collection=database["MYProjectTEST"]
				dictionary={'_id': help3,"Type":test,"Defects":test1,"Colour":test2,"coordinates":(0,0),"Reaching_Time":Rech_time,"Link":name}
				collection.insert_one(dictionary) 
				help2=help2+1

		t2=cv.getTickCount()
		print((t2-t1)/cv.getTickFrequency())
        
		# Display the resulting frame
		cv.imshow("initial", initial)
		help2=0
		help1+=1
		currentframe+=1
		

	# Press Q on keyboard to exit
		if cv.waitKey(1000) & 0xFF == ord('q'):
			break	

# Break the loop
	else:
		print("Capture of image get stoped")
		break


# stoping the video
cap.release()

# Closes all the frames
cv.destroyAllWindows()