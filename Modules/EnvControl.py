import re

WORDS = ["HEAT","AC","TEMPERATURE","THERMOSTAT"]

PRIORITY = 3

def handle(text, mic, profile, house):
    text = text.upper()
    if "CURRENT" in text:
        if "SETTING" in text:
            mic.say(str.format("The thermostat is currently set to {0} degrees", house.therm.getTempSetting()))
        elif "TEMPERATURE" in text:
            mic.say(str.format("The current temperature is {0} degrees", house.therm.getTemp()))
        
    elif "SET" in text:
        temp = int(re.search(r'\d+',text).group(0))
        if temp is not None :
            house.therm.setTempSetting(temp)
            mic.say(str.format("setting the thermostat to {0} degrees", temp))
        else  :
            mic.say(str.format("I did not get a new temperature to set the thermostat"))
            
    elif any(s in text for s in ["AC","HEAT","OFF"]):
        if "OFF" in text:
            mic.say("turning off the heating and air conditioning")
            house.therm.setStatus(0)
        elif "AC" in text :
            mic.say("turning on the air conditioner")
            house.therm.setStatus(2)
        elif "HEAT" in text:
            mic.say("turning on the heat")
            house.therm.setStatus(1)
        
def isValid(text):
    return any(word in text.upper() for word in WORDS)
