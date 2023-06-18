# import modules
import numpy as np
import pymongo
from pyfirmata import Arduino, SERVO
import math
import time

# data reciver
client=pymongo.MongoClient("mongodb://localhost:27017")
database=client["Project"]
collection=database["ProjectTEST"]

# ardino connection
# port
pin1=8
pin2=9
pin3=10
pin4=11

# connection port
port="COM4"

# connection
board=Arduino(port)
board.digital[pin1].mode=SERVO
board.digital[pin2].mode=SERVO
board.digital[pin3].mode=SERVO
board.digital[pin4].mode=SERVO

# inverse kinematics
def Inverse(X,Y,ang):
    # Length of links in cm
    a1 = float(input('')) #link 1 length
    a2 = float(input('')) #link 2 length
    a3 = float(input('')) #link 3 length

    # Desired Position of End effector
    px = float(X)
    py = float(Y)

    phi = float(ang)
    phi = np.deg2rad(phi)

    # Equations for Inverse kinematics
    wx =px - a3*((np.cos(phi)))
    wy = py - a3*((np.sin(phi)))

    delta =(wx*2 + wy*2)
    c2 = ( delta -a1*2 -a2*2)/(2*a1*a2)
    s2 = (np.sqrt(1-c2**2) ) # elbow down
    theta_2 = (np.arctan2(s2, c2))#tan inverse of s2/c2

    s1 = ((a1+a2*c2)*wy - a2*s2*wx)/delta
    c1 = ((a1+a2*c2)*wx + a2*s2*wy)/delta
    theta_1 = (np.arctan2(s1,c1))
    theta_3 = phi-theta_1-theta_2


    a=math.degrees(theta_1)
    b=math.degrees(theta_2)
    c=math.degrees(theta_3)

    return list(a,b,c)


def rotate(pin,angle):
    board.digital[pin].write(angle)
    time.sleep(0.015)

def angle1(pin,angle):
    for i in range(0,angle):
        rotate(pin,i)

def angle2(pin,angle):
    for i in range(angle,0,-1):
        rotate(pin,i)        

while True:
    help1=1
    all_data=collection.find_one("_id"[help1])
    if (all_data["Defects"]==True and all_data["Colour"]==False) or (all_data["Defects"]==False and all_data["Colour"]==None):
        cord=all_data["coordinates"]
        Time=all_data["Reaching_Time"]
        t=time.localtime()
        current_time=int(time.strftime("%S",t))
        if current_time!=Time:
            Wait=Time-current_time
            time.sleep(Wait)

        data1=Inverse(cord[0],cord[1],cord[2])

        # home to tarket posstion
        angle1(pin1,data1[0])
        angle1(pin2,data1[1])
        angle1(pin3,data1[2])
        angle1(pin4,30)

        # tarket postion to new position
        angle2(pin3,90)
        angle2(pin1,140)
        angle1(pin4,60)

        # new position to home position
        angle1(pin1,90)
        angle1(pin2,90)

        help1+=1    

