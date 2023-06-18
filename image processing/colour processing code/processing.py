import numpy as np
import cv2 as cv


def rectangle(frame):

	rectangle_ref=40000

	hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

	lower = np.array([50, 50, 20])
	upper = np.array([100, 255, 255])

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
	
	if base<rectangle_ref:
		test1="complete burn"

	elif base>rectangle_ref and base<30000:
		test1="half burned"

	else:
		test1="normal"

	return test1	


def square(frame):

	square_ref=40000

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
	
	if base<square_ref:
		test1="complete burn"

	elif base>square_ref and base<30000:
		test1="half burned"

	else:
		test1="normal"

	return test1

def circle(frame):

	circle_ref=40000

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
	
	if base<circle_ref:
		test1="complete burn"

	elif base>circle_ref and base<30000:
		test1="half burned"

	else:
		test1="normal"

	return test1	