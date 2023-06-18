""" This program is to capture the frame and save the frame in jpg form """

# importing modules
import numpy as np
import cv2 as cv
import threading as th

# capturing video
cap = cv.VideoCapture(0)

# video no/off  recording checking
if (cap.isOpened()== False):
	print("Error opening video file")
	exit()

""" this stage "view_mode" displaying the frame and Image_capture
    get capture frame simultaneously and save as jpg form with 
	file name as"Frame(0-n).jpg" """

def Image_capture():

	currentframe=0 # frame number

	while(cap.isOpened()):
		ret, frame = cap.read() # frame read

		if ret == True:	

			name = 'FRAME' + str(currentframe) + '.jpg' # frame name
			cv.imwrite(name, frame) # frame save
			
			key=cv.waitKey(25) # new windows display time
			if key == 113: # press Key "Q" to stop 
				break
			
		else:
			print("Capture of image get stoped")
			break
		
	cap.release()  # stop recording in image_capture
	cv.destroyAllWindows() # close all open windows in image_capture



# In View_mode it get display frame only cannot performly don't perform an action
def view_mode():

	while(cap.isOpened()):
	
		ret, frame = cap.read() # frame read
		if ret == True:
			
			cv.imshow("Frame",frame) # display the frame

			if cv.waitKey(25) & 0xFF == ord('q'): # new windows display time & press Key "Q" to stop
				break

		else:
			print("Capture of image get stoped")
			break

	cap.release() # stop recording in view_mode
	cv.destroyAllWindows() # close all open windows in view-mode

# performing the action simultaneously
t1 = th.Thread(target=view_mode)  # calling the view_mode first
t2 = th.Thread(target=Image_capture)  # after that image_capture 

t1.start() # starting View_mode
t2.start() # starting Image_capture 