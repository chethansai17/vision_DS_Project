from pyfirmata import ArduinoMega, SERVO
import time
port='COM3'
pin=9

board=ArduinoMega(port)
board.digital[pin].mode=SERVO

def rotate(pin,angle):
    board.digital[pin].write(angle)
    time.sleep(0.015)

def angle1(angle):
    for i in range(0,angle):
        rotate(pin,i) 
    for i in range(angle,0,-1):
        rotate(pin,i)    


angle1(90)