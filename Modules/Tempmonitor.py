import smbus
import RPi.GPIO as GPIO
from time import sleep
import threading
#import random

class TempMonitor:
    
    
    def __init__(self, temp = 65):
        self.THERM = 24
        self.bus = smbus.SMBus(1)
        self.tempSetting = temp
        self.ambientTemp = self.getAmbientTemp()
        self.status = 1
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.THERM, GPIO.OUT)
        GPIO.output(self.THERM, GPIO.LOW)
        
        self.event = threading.Event()
        self.alive = True
        self.thread = threading.Thread(target=self.monitor, args = (self.event, self.status, self.getTempSetting))
        self.thread.setDaemon(True)
        self.thread.start()
        
        
    def getAmbientTemp(self):
    #get the current temperature from the sensor
        temp = self.bus.read_byte(0x48)
        #temp = random.uniform(20, 30)
        self.ambientTemp = int((temp * 1.8) + 32)
        #print "It is currently : ", self.ambientTemp
        return self.ambientTemp
        
    def setTempSetting(self, temp):
    #set the desired temperature
        self.tempSetting = temp
        self.event.set()
        
    def getTempSetting(self):
        return self.tempSetting
        
    def getTemp(self):
    #get the current room temperature without pinging sensor
        return self.ambientTemp
        
    def setStatus(self,hvac):
        #sets AC(2) or Heating(1)
        self.status = hvac
        self.event.set()
        
    def getStatus(self):
        return self.status
        
    def monitor(self, event, status, temp):
    #Constantly monitor the temperature and set the heater or AC as needed
        status = status
        temp = temp
        #print "Starting to monitor the system :", self.getTempSetting()
        while(self.alive):
            #if thermostat set to heat turn it on when room temp lower than desired
            if(status == 1):
                if (temp > self.getAmbientTemp()):
                    GPIO.output(self.THERM, GPIO.HIGH)
                    #print "Turning on the heat"
                else:
                    GPIO.output(self.THERM, GPIO.LOW)
                    print "Turning off the heat"
            #if thermostat set to AC turn it on when room temp higher than desired
            elif(status == 2):
                if(temp < self.getAmbientTemp()):
                    GPIO.output(self.THERM, GPIO.HIGH)
                    #print "Turning on the AC"
                else:
                    GPIO.output(self.THERM, GPIO.LOW)
                    #print "Turning off the AC"
            #Only poll the temp sensor every 30 seconds
            elif(status == 0):
                GPIO.output(self.THERM, GPIO.LOW)
            sleep(30)
            if(event.wait(1)):
                event.clear()
                status = self.getStatus()
                temp = self.getTempSetting()
                #print "Received new values : ", status, " / " , temp
                
    def cleanUp(self):
        self.alive = False
        self.thread.join()
        GPIO.cleanup()
        
#test module
"""
test = TempMonitor(90)
sleep(5)
print "Changing the set temperature : 75"
test.setTempSetting(60)
sleep(10)
print "Changing to AC"
test.setStatus(2)
sleep(10)
print "Current temp variable is: ", test.getTemp()
print "Current setting is : ", test.getStatus()
print "Current temp is : " , test.getAmbientTemp()
print "Current temp variable is : ", test.getTemp()
test.cleanUp()
"""