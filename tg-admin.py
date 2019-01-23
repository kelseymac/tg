from tg import Venue, Event, venues, events, save, load

def main_menu():
    print("1. Create venue")
    print("2. Create event")
    print("3. Delete event")
    print("4. QUIT")

def create_venue():
    try:
        venue_name = input("Venue name? ")
        num_seats = int(input("How many seats? "))
        new_venue = Venue(venue_name, num_seats)
        venues[venue_name] = new_venue
    except ValueError:
        print("\n" + "Please type a number for the seats option." + "\n")
        create_venue()
        
def create_event():
    try:
        event_name = input("Event name? ")
        venue_name = input("Venue name? ")
        venue = venues[venue_name]
        new_event = Event(event_name, venue)
        events[event_name] = new_event
    except KeyError:
        print("\n" + "Please, try again." +"\n")    
    
def delete_event():
    name = input("Name of event? ")
    try:
        if name in events:
            del events[name] 
    except KeyError:
        print("Sorry, that event does appear in our listings")




QUIT_NUM = 4
load()
#print(events)
main_menu()
choice = int(input("Choice? "))
while choice != QUIT_NUM:
    if choice == 1:
        create_venue()
    elif choice == 2:
        create_event() 
    elif choice == 3:
        delete_event()
    else:
        print("\n" + "That option is not available. Please, try again." + "\n")        
    #print(venues)
    main_menu()
    choice = int(input("Choice? "))

save()
print("Done. Exiting.")



