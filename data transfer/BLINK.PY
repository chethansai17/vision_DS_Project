from pyfirmata import ArduinoMega, SERVO, util
from time import sleep

port='COM4'
pin=10
board=ArduinoMega(port)

board.digital[pin].mode=SERVO

def rotateservo(pin,angle):
    board.digital[pin].write(angle)
    sleep(0.015)

rotateservo(10,180)    
        