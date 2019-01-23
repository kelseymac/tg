class Venue:
    def __init__(self, name, num_seats):
        self.name = name
        self.num_seats = num_seats
        self.events = {}

    def __str__(self):
       # return "Venue:name=%s,seats=%d" % (self.name, self.num_seats)
        pass
    def __repr__(self):
       # return self.__str__()
        pass

class Event:
    def __init__(self, name, venue):
        self.name = name
        self.venue = venue
        # Example: [7, 8, 9, ..., 149]
        self.avail_seats = []
        # Example: { "mccokel@bvu.edu": [1, 2, 3, 4], "shepherd@bvu.edu": [5, 6] }
        self.assign_seats = {}

    def __str__(self):
       # return "Event:name=%s,venue=%s" % (self.name, self.venue)
        pass
    def __repr__(self):
       # return self.__str__()
        pass
venues = {}
events = {}

def save():
    # Write the contents of our venues and events dictionaries
    # into tg-venues.txt and tg-events.txt.
    # Refer to the image on Slack titled "Files (data)" for the 
    # format of these files.
    v  = open("tg-venues.txt", "w")
    for venue in venues.values():
        v.write(venue.name + "," + str(venue.num_seats) + "\n")
    v.close()

    e = open("tg-events.txt", "w")
    for event in events.values():
        e.write(event.name + "," + event.venue.name + "\n")
    e.close()
    
def load():
    v = open("tg-venues.txt", "r")
    v_s = v.readline()
    while v_s != "":
        things = v_s.rstrip().split(",")
        venue = Venue(things[0], int(things[1]))
        venues[venue.name] = venue
        v_s = v.readline()
    v.close()
    
    e = open("tg-events.txt", "r")
    e_v = e.readline()
    while e_v != "":
        things = e_v.rstrip().split(",")
        event = Event(things[0], venues[things[1]])
        events[event.name] = event
        e_v = e.readline()
    e.close()

