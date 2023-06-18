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

def process(frame,data2):

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    lower = np.array([15, 50, 0])
    upper = np.array([170, 255, 255])

    mask = cv.inRange(hsv, lower, upper)
    result = cv.bitwise_and(frame, frame, mask=mask)

    base=0
    for i in result:
        a=np.array([0,0,0])

        for j in i: 
            compare=np.array_equal(a,j)

            if compare==True:
                continue

            else:
                base+=1   
    
    if base<data2:
        test4=False
        print("complete burn")

    else:
        test4=True
        print("normal")
	
    return test4 
   
# input parameters
# rectangle
Length_rectangle1=108 # length
Length_rectangle2=117
width_rectangle1=177 
width_rectangle2=188 # width
rectangle_range1,rectangle_range2=10000,20000  # area of rectangle varies

# square
square_range1,square_range2=20000,30000
size=160

# circleq
circles_area1,circles_area2=50000,60000
major_radius=85
minor_radius=75

# collor detection
Colour={"Rectangle":5000,"Square":5000,"Circle":6000}
Colour1={"Rectangle":5000,"Square":5000,"Circle":6000}

#colour data
Rect_colour=5000
Squ_colour=4000
Cir_colour=6000

# image save numbers
currentframe=0
# camera calibration

# object reach
RB_Resp_Time=2 # robot responce time in seconds
conevory_speed= 2.5 # Converoy speed in cm/min
conevory_dist= 30 # Distance travel in cm

# Helping varibles
help1=1


# Read until video is completed
while(cap.isOpened()):
	
    # Capture frame-by-frame
	ret, initial = cap.read()
	if ret == True:

		name = 'C:/storage/FRAME' + str(currentframe) + '.jpg' # frame location

		initial = cv.medianBlur(initial,5)
        # object detection
		imgray = cv.cvtColor(initial, cv.COLOR_BGR2GRAY)
		ret,treshold = cv.threshold(imgray,120,255,cv.THRESH_BINARY)
		
        # object location
		contours, hierarchy = cv.findContours(treshold, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
		
        # No object present
		if len(contours)==0:
			print("object is not found")
			continue
		
		else:
			# object detect
			for i in contours:
				if len(i) in range(400,600):
					print("yes")
					x,y,w,h=cv.boundingRect(i)
					
                    # center points of object
					M = cv.moments(i)
					if M['m00'] != 0:
						cx1 = int(M['m10']/M['m00'])
						cy1 = int(M['m01']/M['m00'])
						cv.putText(initial,str(help1),(cx1,cy1),cv.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2,cv.LINE_AA)

                    # object segmentation
					frame=initial[y-6:y+h+6,x-6:x+w+6]
					imgray1 = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
					ret,treshold1 = cv.threshold(imgray1,120,255,cv.THRESH_BINARY)
					
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
							
					main_zone=contour1[index]
					approx = cv.approxPolyDP(main_zone, 0.01*cv.arcLength(main_zone, True), True) # collect edge points

                    # rectangle & square
					if len(approx) == 8 or len(approx)==4 :
						
                        # collecting positions
						x1,y1,w1,h1=cv.boundingRect(main_zone)
						length=(x1+w1)-x1
						width=(y1+h1)-y1
						aspect_ratio = float(w1) / float(h1)
						area=cv.contourArea(main_zone)
						cv.rectangle(frame,(x1,y1),(x1+w1,y1+h1),(0,255,0),1)

                        # sqaure code
						if aspect_ratio >= 0.95 and aspect_ratio <= 1.05: # center moment is same 
							test="Square"
							print(test)

							if (area in range (square_range1,square_range1)) and length==149 and width==153 : 
								test1=True
								print("No Defects")
								
                                # Color Detection
								test2=process(frame,Squ_colour)
								
							else:
								test1=False
								test2=None
								print("Defect")
								
                        # rectangle code        
						else:
							test="Rectangle"
							print(test)
							
                            # checking for dimension satisfaction
							if (area in range(10000,20000)) and (length in range(Length_rectangle1,Length_rectangle2)) and (width in range(width_rectangle1,width_rectangle2)): # checking for dimension satisfaction
								test1=True
								print("No Defects")
								
                                # Color Detection
								test2=process(frame,Rect_colour)
								
							else:
								test1=False
								test2=None
								print("Defect")

                    # Circle Code			
					else:
						test="Circle"
						print(test)
						Area_cir=cv.contourArea(main_zone)
						print(Area_cir)
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
						
						print(minimum,maximum)
						ni=data1.index(minimum)
						le=data1.index(maximum)
						cv.circle(frame,(main_zone[ni].flatten().tolist()),1,(0,255,0),-1)
						cv.circle(frame,(main_zone[le].flatten().tolist()),1,(0,255,0),-1)

                        # desire object sizes 
						if (minimum-maximum)<=(major_radius-minor_radius) and (Area_cir in range(circles_area1, circles_area2)):
							test1=True
							print("No Defects")
							
                            # Color Detection
							test2=process(frame,Cir_colour)
							data1.clear()
							
							
						else:
							test1=False
							test2=None
							print("Defect")

				    # object Reaching time
					Rech_time=(conevory_dist/conevory_speed) - RB_Resp_Time
					print(Rech_time)
					t=time.localtime()
					current_time=time.strftime("%S",t)
					Rech_time1=Rech_time+int(current_time)

					
                    # data storge
					client=pymongo.MongoClient("mongodb://localhost:27017")
					database=client["Project"]
					collection=database["ProjectTEST"]
					dictionary={'_id':help1 ,"Type":test,"Defects":test1,"Colour":test2,"coordinates":(0,0),"Reaching_Time":Rech_time,"Link":name}
					collection.insert_one(dictionary) 
					help1+=1

		# Image save    
		cv.imwrite(name, initial) # frame save
		
        # Display 
		cv.imshow("initial", initial)
		cv.imshow("frame", frame)
		
		currentframe+=1
		
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