


WORDS = ["LIGHTS", "LIGHT"]

Rooms = ['Living','Dining','Kitchen']
Status = ['Off','On','Dim','Raise']

def handle(text, mic, profile, house):
    text = text.upper()
    room = None
    status = None
    print text
    room = 1 if "LIVING" in text else room
    room = 2 if "DINING" in text else room
    room = 3 if "KITCHEN" in text else room
    status = 1 if "OFF" in text else status
    status = 2 if "ON" in text else status
    status = 3 if "DIM" in text else status
    status = 4 if "UP" in text else status
    room = 2 if "MOOD" in text else room
    status = 2 if "MOOD" in text else status
    room = 1 if "MOVIE" in text else room
    status = 2 if "MOVIE" in text else status
    print str.format("Room : {0}\nStatus : {1}\n",room,status)
    if status and room:
        print str.format("Changing the lights in {0} to {1}", Rooms[room-1], Status[status-1])
    else:
        print "I'm sorry, I did not get a room or status"
    return
    
def isValid(text):
    return any(word in text.upper() for word in WORDS)
	

	
	
def test():
    print isValid("lights")
    print isValid("LIGHTS")
    print isValid("bulbs")
    print isValid("turn up the living room lights")
    handle("turn up the living room lights", None, None)
    handle("dim the living room lights",None, None)
    handle("mood lights",None,None)
    handle("set the lights for a movie",None,None)
    handle("turn on the kitchen lights",None,None)
    return
	
test()
