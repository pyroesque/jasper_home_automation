import RPi.GPIO as GPIO
from time import sleep

class Lights:
    

    def __init__(self):
        #constant definitions
        LIVING = 21
        KITCHEN = 23
        DINING = 22
        #setup the GPIO pins
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(LIVING, GPIO.OUT)
        GPIO.setup(DINING, GPIO.OUT)
        GPIO.setup(KITCHEN, GPIO.OUT)
        self.lr = GPIO.PWM(LIVING, 50)
        self.ki = GPIO.PWM(KITCHEN, 50)
        self.dr = GPIO.PWM(DINING, 50)
        self.lr.start(1)
        self.ki.start(1)
        self.dr.start(1)
        
    def off(self,room):
        if room == 1:
            self.lr.ChangeDutyCycle(1)
        elif room == 2:
            self.dr.ChangeDutyCycle(1)
        elif room == 3:
            self.ki.ChangeDutyCycle(1)
            
    def on(self,room):
        if room == 1:
            self.lr.ChangeDutyCycle(100)
        elif room == 2:
            self.dr.ChangeDutyCycle(100)
        elif room == 3:
            self.ki.ChangeDutyCycle(100)
            
    def var(self, room, cycle):
        if room == 1:
            self.lr.ChangeDutyCycle(cycle)
        elif room == 2:
            self.dr.ChangeDutyCycle(cycle)
        elif room == 3:
            self.ki.ChangeDutyCycle(cycle)
           
    def clean(self):
        self.lr.stop()
        self.dr.stop()
        self.ki.stop()
        GPIO.cleanup()
        
    """
    def __del__(self):
        lr.stop()
        dr.stop()
        ki.stop()
        GPIO.clean()
       """ 
        
        

"""
test = Lights()
for i in range(1,4):
    print "Room off : ", i
    test.off(i)
    sleep(1)
for i in range(1,4):
    print "Room on : ", i
    test.on(i)
    sleep(1)
for i in range(1,4):
    print "Room var : ", i
    test.var(i,50)
    sleep(1)
for i in range(1,4):
    print "Room off : ", i
    test.var(i, 75)
    sleep(1)
for i in range(1,4):
    test.off(i)
    sleep(1)
test.clean()
"""