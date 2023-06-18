# In this python file the frame get read and saved in the video form.

# importing libraries
import numpy as np
import cv2 as cv

# Create a VideoCapture object and read from input file
cap = cv.VideoCapture(0)
fourcc=cv.VideoWriter_fourcc(*'DIVX') 
out = cv.VideoWriter('project.avi', fourcc, 25, (640, 480))

# Check if camera opened successfully
if (cap.isOpened()== False):
	print("Error opening video file")

# Read until video is completed
while(cap.isOpened()):
	
# Capture frame-by-frame
	ret, frame = cap.read()
	if ret == True:
		
        # save the frame
		# out.write(frame)
		
	# Display the resulting frame
		cv.imshow('Frame', frame)
		
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
