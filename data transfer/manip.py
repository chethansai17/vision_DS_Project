from pyfirmata import ArduinoMega, SERVO
import time 


# port
pin1=8
pin2=9
pin3=10
pin4=11

# connection port
port="COM3"

# connection
board=ArduinoMega(port)
board.digital[pin1].mode=SERVO
board.digital[pin2].mode=SERVO
board.digital[pin3].mode=SERVO
board.digital[pin4].mode=SERVO

# calling for an action
def rotate(pin,angle):
    board.digital[pin].write(angle)
    time.sleep(0.015)

def angle1(pin,angle):
    for i in range(0,angle):
        rotate(pin,i) 

# home to tarket posstion
angle1(pin1,90)
angle1(pin2,90)
angle1(pin3,90)
angle1(pin4,90)

# tarket postion to new position
angle1(pin1,90)
angle1(pin2,90)
angle1(pin3,90)
angle1(pin4,90)

# new position to home position
angle1(pin1,90)
angle1(pin2,90)
angle1(pin3,90)
angle1(pin4,0)
