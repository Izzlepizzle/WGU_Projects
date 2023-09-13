# WGUPS Delivery Algorithm
# Author: Nathan Perkins
# August 30, 2022
# PyCharm 2022.2 (Community Edition)
# Build #PC-222.3345.131, built on July 27, 2022
# Runtime version: 17.0.3+7-b469.32 x86_64
# VM: OpenJDK 64-Bit Server VM by JetBrains s.r.o.
# macOS 12.4
# GC: G1 Young Generation, G1 Old Generation
# Memory: 2048M
# Cores: 8
# Metal Rendering is ON
# Python 3.1

from Package import hashTab
from Destination import *
from Truck import *
from datetime import datetime, time, date, timedelta
from Interface import interface

# Creates truck objects
truck_1 = Truck("Truck 1")
truck_2 = Truck("Truck 2")
truck_3 = Truck("Truck 3")
# Creates set for visited destinations
visited = set()
# Creates a set for ineligible destinations
ineligible = set()
# Creates a start time for trucks
start = time(8, 0)
start_time = datetime.combine(date.today(), start)
# truck3_start = datetime.combine(date.today(), time(9, 30))
# Creates variables for user input
input_id = 0
input_time = time()
user = interface()
# Default time
t = time(23,0,0)

# Fixes the address on the incorrect address package
hashTab.set_address(9, "410 S State St.", 18)


# This is the main algorithm for the program. It takes a trucks deque and one by one adds packages from the next
# nearest destination. It takes a truck type object as it's only parameter
def load_packages(truck):
    # ineligible is a set of destinations that will not work in the route
    ineligible.clear()
    # visited is a set of destinations that have been visited already
    visited.add(0)
    # This loops while the truck still has room and there are still destinations to visit.
    while len(truck.packages) < 16 and len(visited) < len(destinations) and len(visited) + len(ineligible) < len(destinations):
        #print("Loop start")
        # This first operation checks for the nearest eligible destination to the HUB
        if len(truck.packages) > 0:
            p = truck.packages[len(truck.packages) - 1]
            next_id = nearest(p.p_id, visited, ineligible)
        else:
            next_id = nearest(0, visited, ineligible)
        # This line creates a list of any packages that go to the next nearest destination
        p_list = same_dest(next_id)
        #print(next_id)
        #print(p_list)
        #print(is_special(p_list))
        # This checks to make sure that the list of eligble packages can fit on the truck. If not then the destination is added to ineligible
        if len(truck.packages) + len(p_list) <= 16:
            # Next we check for any special conditions. All non truck specific special packages are added to truck 3
            # Check the is_special and load_list methods for more details on how those work
            if is_special(p_list) == '':
                load_list(truck, p_list, next_id)
            elif is_special(p_list) == "Can only be on truck 2" and truck.name == "Truck 2":
                load_list(truck, p_list, next_id)
            elif truck.name == "Truck 3":
                load_list(truck, p_list, next_id)
            else:
                ineligible.add(next_id)
        else:
            ineligible.add(next_id)

        #print(len(truck.packages))
        #print(len(visited))
        #print(visited)


# This method creates a list of packages going to the same destination
# It takes an destination id as the only parameter
# It iterates through the range of the size of the hash table where packages are stored
def same_dest(p_id):
    new_list = []
    for p in range(1, hashTab.size + 1):            # Iterates through every package in the hash table
        pack = hashTab.get(p)                       # Creates a package object from the hash table
        if pack.p_id == p_id and pack.id != 9:      # Checks to see if the destination id matches the given id or if it is package number 9
            new_list.append(p)                      # Adds the package to the list

    return new_list


# This method returns a string of any special notes in a list of packages
def is_special(list):
    for i in list:
        pack = hashTab.get(i)       # Gets the package data from hash table
        #print(pack.special)
        if pack.special != '':      # Checks the special value for the package
            #print(pack.special)
            return pack.special     # returns that value as a string
        else:
            return ''               # Returns a blank string if nothing is found


# This method does the actual loading into the deque of a given truck
# It iterates through a given list adding each element to the deque
def load_list(truck, p_list, next_id):
    if len(truck.packages) + len(p_list) <= 16:         # Checks to make sure that the list does not exceed truck capacity
        for p in p_list:
            new_pack = hashTab.get(p)                   # Creates a package object from the hash table
            #print(new_pack.special)
            if new_pack.status == "Depot" and new_pack not in truck.packages:   # Checks that the package is not a duplicate
                truck.add_package(new_pack)         # Adds the package to the truck
                #print("Package added")
                #print(new_pack.id)
                hashTab.set_status(new_pack.id, truck.name)         # Sets the package status to the truck
                visited.add(next_id)                                # Adds the current location to the visited set
    else:
        ineligible.add(next_id)                                     # If it is not added then the location is added to ineligible


# This method actually calculates the delivery time and distanced traveled by each truck.
# It looks up distances from the distance table and adds them to the total.
# Then it calculates the time of delivery based off of distance and the speed of the truck.
# It also doesn't let truck 3 leave until at least one truck has finished.
def distance_traveled(truck, target_time):
    # Sets truck 3 start time to whenever one of the other trucks finish
    if truck.name == "Truck 3":
        s_time = truck_1.finished_time if truck_1.finished_time < truck_2.finished_time else truck_2.finished_time
        #print(s_time)
    else:
        s_time = start_time
    #print(target_time)
    # checks to see if there is a specific timeframe that we want to see package status.
    # If not then it will show package data at the end of day
    if target_time == '':
        #print("Converting time")
        target_time = datetime.combine(date.today(), t)
        #print(target_time)
    packages = truck.packages
    total = 0.0
    length = len(packages)
    # Starts a loop iterating through the list of the packages
    for p in range(length):
        # Looks up the package in the deque
        pack = packages[p]
        # If it is the first package then it compares distance to the Hub
        if p == 0:
            if distance_array[pack.p_id][0] != '':              # Checks first side of 2 sided array
                total += float(distance_array[pack.p_id][0])    # Adds distance to the total
                time = total / truck.speed                      # Calculates time based on total distance traveled
                delivered_time = s_time + timedelta(minutes=time)  # Adds the time traveled to the start time to get the delivered time
                if delivered_time.time() < target_time.time() or target_time == '':  # checks to see if the delivered time is before the target time
                    hashTab.set_status(pack.id, f"Delivered at {delivered_time.time()}")  #Sets the package status to delivered at (Delivered time)
            else:                                               # Checks the other side of the array
                total += float(distance_array[0][pack.p_id])    # Adds distance to the total
                time = total / truck.speed                      # Calculates time based on total distance traveled
                delivered_time = s_time + timedelta(minutes=time) # Adds the time traveled to the start time to get the delivered time
                if delivered_time.time < target_time.time: # checks to see if the delivered time is before the target time
                    hashTab.set_status(pack.id, f"Delivered at {delivered_time.time()}")  #Sets the package status to delivered at (Delivered time)
        # If it is any other package then it compares distance to the previous destination
        if p < length - 1:
            other = packages[p+1]
            if distance_array[pack.p_id][other.p_id] != '':
                total += float(distance_array[pack.p_id][other.p_id])    # Adds distance to the total
                time = total / truck.speed                      # Calculates time based on total distance traveled
                delivered_time = s_time + timedelta(minutes=time) # Adds the time traveled to the start time to get the delivered time
                if delivered_time.time() < target_time.time(): # checks to see if the delivered time is before the target time
                    hashTab.set_status(pack.id, f"Delivered at {delivered_time.time()}")  #Sets the package status to delivered at (Delivered time)
            else:
                total += float(distance_array[other.p_id][pack.p_id])    # Adds distance to the total
                time = total / truck.speed                      # Calculates time based on total distance traveled
                delivered_time = s_time + timedelta(minutes=time) # Adds the time traveled to the start time to get the delivered time
                if delivered_time.time() < target_time.time(): # checks to see if the delivered time is before the target time
                    hashTab.set_status(pack.id, f"Delivered at {delivered_time.time()}")  #Sets the package status to delivered at (Delivered time)
        else:   # This code calculates the distance from the final destination back to the Hub
            if distance_array[pack.p_id][0] != '':
                total += float(distance_array[pack.p_id][0])    # Adds distance to the total
                time = total / truck.speed                      # Calculates time based on total distance traveled
                delivered_time = s_time + timedelta(minutes=time) # Adds the time traveled to the start time to get the delivered time
                if delivered_time.time() < target_time.time() or target_time == '': # checks to see if the delivered time is before the target time
                    hashTab.set_status(pack.id, f"Delivered at {delivered_time.time()}")  #Sets the package status to delivered at (Delivered time)
            else:
                total += float(distance_array[0][pack.p_id])    # Adds distance to the total
                time = total / truck.speed                      # Calculates time based on total distance traveled
                delivered_time = s_time + timedelta(minutes=time)  # Adds the time traveled to the start time to get the delivered time
                if delivered_time.time < target_time.time: # checks to see if the delivered time is before the target time
                    hashTab.set_status(pack.id, f"Delivered at {delivered_time.time()}")  #Sets the package status to delivered at (Delivered time)

    truck.finished_time = delivered_time    # Sets the finish time for the truck
    return round(total, 2)                  # Returns the total distance traveled


# This method handles interaction and input from the user
def user_interface():
    print("Welcome to the WGUPS Delivery Tracker!")
    selection = ""
    success = False
    # Program loops while there is an invalid input
    while not success:
        # Collects user input here
        selection = int(input("To see the information for a specific package please enter 1. To see the status of all packages at a given time press 2."
                          "To see distance traveled for all trucks today enter 3.  "))
        # if user selects 1 then this code executes
        if selection == 1:
            # Asks for user input on package id and time
            user.set_id()
            user.set_time()
            # executes the distance traveled method for each truck
            distance_traveled(truck_1, user.time)
            distance_traveled(truck_2, user.time)
            distance_traveled(truck_3, user.time)
            # Grabs the requested package from the hash table
            out = hashTab.get(user.id)
            # Outputs to the console the package information and the requested time
            print(f"Status of package {out.id} at {user.time}")
            print(f"ID: {out.id}, Address: {out.address}, Deadline: {out.deadline}, City: {out.city}, Zip: {out.zip}, "
                  f"Weight: {out.weight}, Status: {out.status}")
            success = True
        # If the user selects 2 then this code executes
        elif selection == 2:
            # Asks the user for a time
            user.set_time()
            # executes the distance_traveled method for each truck at the given time
            distance_traveled(truck_1, user.time)
            distance_traveled(truck_2, user.time)
            distance_traveled(truck_3, user.time)
            # prints information for every package at the selected time
            print(f"All packages at {user.time}")
            for i in range(1, 41):
                out = hashTab.get(i)
                print(f"ID: {out.id}, Address: {out.address}, Deadline: {out.deadline}, City: {out.city}, Zip: {out.zip}, "
                    f"Weight: {out.weight}, Status: {out.status}")
            success = True

        # Executes if the user selects 3
        elif selection == 3:
            # Prints to console the total distance traveled for each truck
            print("Truck 1 distance traveled:")
            print(distance_traveled(truck_1, ''))
            print("Truck 2 distance traveled:")
            print(distance_traveled(truck_2, ''))
            print("Truck 3 distance traveled:")
            print(distance_traveled(truck_3, ''))
            success = True
        else:
            print("Invalid input. Please try again.")


# Here we actually execute the code needed to deliver the packages.
load_packages(truck_1)
load_packages(truck_2)
load_packages(truck_3)
# Package 9 is added last since the correct address is not known until much later
pack = hashTab.get(9)
truck_3.packages.append(pack)
hashTab.set_status(9, truck_3.name)
#print(pack.special)

# Executes the user interface method
user_interface()

# print statements for troubleshooting
#distance_traveled(truck_1, '')
#distance_traveled(truck_2, '')
#distance_traveled(truck_3, '')
#for i in range(1, 41):
#    out = hashTab.get(i)
#    print(f"ID: {out.id}, Address: {out.address}, Deadline: {out.deadline}, City: {out.city}, Zip: {out.zip}, "
#          f"Weight: {out.weight}, Status: {out.status}")
