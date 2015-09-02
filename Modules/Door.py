import serial
import RPi.GPIO as GPIO
import threading

class Door:

    def __init__(self, mic):
        self.ver = 0b11010000
        self.lock = 0b00000001
        self.open = 0b00000010
        self.bell = 0b00000100
        self.legit = 0b00001001
        self.bad = 0b00001000
        self.ser = serial.Serial("/dev/ttyAMA0", baudrate=9600)
        self.ser.flushInput()
        self.door = ""
        self.valid = True
        self.mic = mic
        self.DOOR = 26
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.DOOR, GPIO.OUT)
        GPIO.output(self.DOOR, GPIO.LOW)
        self.thread = threading.Thread(target=self.work)
        self.thread.setDaemon(True)
        self.thread.start()
        
    def getStatus(self):
        return self.door
        
    def setValid(self,status):
        self.valid = status
        
    def work(self):
        while(self.valid):
            if(self.ser.inWaiting() > 0):
                status = ord(self.ser.read(1))
                if (status & 0b11110000) | self.ver == self.ver:
                    control = (status & 0b00001111)
                    prev = self.door
                    say = ""
                    #print(control)
                    #print(status)
                    if control == 0b00000000:
                        self.door = "normal"
                        say = "The door is closed and locked."
                        GPIO.output(self.DOOR, GPIO.LOW)
                    elif control == self.open:
                        print("open")
                        self.door = "open"
                        say = "The door is opened."
                        GPIO.output(self.DOOR, GPIO.HIGH)
                    elif control == self.bell:
                        print("visitor")
                        self.door = "visitor"
                        say = "There is a visitor at the door."
                    elif control == self.legit:
                        print("key")
                        self.door = "key"
                        say = "The door is unlocked, welcome home"
                        GPIO.output(self.DOOR, GPIO.HIGH)
                    elif control == self.bad:
                        print("bad")
                        self.door = "bad"
                        say = "An invalid key was used at the door"
                        GPIO.output(self.DOOR, GPIO.LOW)
                    elif  control == self.lock:
                        print("unlocked")
                        self.door = "unlocked"
                        say = "The door is unlocked"
                        GPIO.output(self.DOOR, GPIO.HIGH)
                    if prev != self.door:
                        self.mic.say(say)
            
"""test = Door()
test.work()"""