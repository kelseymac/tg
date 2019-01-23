from tg import Venue, Event, venues, events, save, load
import re
import smtplib

def reserve(event_name, want_seats, email):
    # Assign seats from the available seats for this event.
    # In other words
    #   1. lookup the Event object using the event_name.
    event = events[event_name]

    #   2. remove available seats from the event.
    #   3. assign those removed seats to the person in the assign_seats dict.
    if want_seats > len(event.avail_seats):
        print("Sorry, there are only %d seats left. Try again." % len(event.avail_seats))
        return

    event.assign_seats[email] = event.avail_seats[0:want_seats]
    event.avail_seats = event.avail_seats[want_seats:]
    #   4. call save_seats() to save the new seating information for all Events.
    to_addr_list.append(email)
    message = ("Hello %s," + "\n" + "You now have %d seats for %s." + "\n" + "Have a good day!") % (email, want_seats, event_name)
    save_seats()       
    sendemail(from_addr, to_addr_list, [], subject, message, login, password)

def load_seats():
    try:
        s = open("tg-seats.txt", "r")
        sr = s.readline()
        while sr != "":
            things = sr.rstrip().split(",")
            event = events[things[0]]
            event.avail_seats = \
                list(range(event.venue.num_seats-int(things[1]), event.venue.num_seats))
            sr = s.readline()
            while sr != "\n" and sr != "":
                email = sr.rstrip()
                sr = s.readline().rstrip()
                event.assign_seats[email] = list(map(lambda s: int(s), sr.split(","))) 
                sr = s.readline()
            sr = s.readline()
        s.close()
    except:
        # No seats file yet.  Oh well!
        pass

    # If there are any events that have neither available nor assigned seats,
    # create available seats.  This happens when we first create an event that is new.
    for event in events.values():
        if len(event.avail_seats) == 0 and len(event.assign_seats.keys()) == 0:
            event.avail_seats = list(range(0, event.venue.num_seats))

#    print(events)
    

def save_seats():
    s = open("tg-seats.txt", "w")
    for event in events.values():
       # print("trying to save event " + event.name)
       # print("avail seats --> " + str(event.avail_seats))
        s.write(event.name + "," + str(len(event.avail_seats)) + "\n")
        for email in event.assign_seats:
         #   print("Writing seat info for " + email)
          #  print("assigned seat should be " + str(event.assign_seats[email]))
            s.write(email + "\n")
            s.write(",".join(map(lambda i: str(i), event.assign_seats[email])) + "\n")
        s.write("\n")
            
    s.close()


def valid_email(email):
    pattern = "\S+@\S+\.\S+"
    result = re.search(pattern, email)
    if result:
        return True
    else:  
        return False

def sendemail(from_addr, to_addr_list, cc_addr_list,
    subject, message,login, password, smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s \n' % from_addr
    header += 'To: %s \n' % ','.join(to_addr_list)
    header += 'Cc: %s \n' % ','.join(cc_addr_list)
    header += 'Subject: %s \n\n' % subject
    message = header + message

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    print("Sending message:")
    print(message)
    server.quit()

from_addr = 'therealticketgurus@gmail.com'
to_addr_list = []
subject = 'Ticket Order'
login = 'therealticketgurus@gmail.com'
password = 'PASSWORD_HERE'

load()
load_seats()

quit_number = 0
events_list = []

def main_menu():
    global quit_number
    counter = 1
    for event_name in events:
        print("%d. %s" % (counter, event_name))
        events_list.append(event_name)
        counter += 1
    print("%d. QUIT" % counter)
    quit_number = counter

main_menu()
choice = int(input("Choice? "))
while choice != quit_number:
    # If the user chooses an event, you have to subtract 1 from their choice
    # because the index starts at 0.
    try:  
        n = choice - 1
        event_name = events_list[n]
        print("You selected %s." % event_name)
        want_seats = int(input("How many seats would you like? "))
        email = input("Type your email to reserve seats. ")
        if valid_email(email):
            reserve(event_name, want_seats, email)
        else:
            print("Invalid email. Try again.")
    except IndexError:   
        print("\n" + "Please select an option available." + "\n")     
    except ValueError:
        print("\n" + "Please, try again." + "\n")
    
    main_menu()
    choice = int(input("Choice? "))



