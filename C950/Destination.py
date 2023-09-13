from array import *
import csv

class destination:
    def __init__(self, id, address):
        self.id = id
        self.address = address

# This array holds all distances between every location.
# I felt this worked better than a graph since every location connects to every other location.
distance_array = [[]]

# This reads in values from a csv file and adds it to the distances
with open('distances.csv', encoding="utf-8-sig") as csvFile:
    csvReader = csv.reader(csvFile)
    l = 0

    for line in csvReader:
        c = 0
        for column in line:
#            print(column)
            distance_array[l].append(line[c])
            c += 1
        distance_array.insert(l+1, [])
        l += 1

# I used a dictionary for the destination names and ids. It works well for key-value pairs.
# I would have used my hash table, but it was hand tailored for the packages
destinations = {}

# Here we read in the destination names and ids
with open('destinations.csv', encoding="utf-8-sig") as csvFile:
    csvReader = csv.reader(csvFile)
    index = 0
    for line in csvReader:
        d = destination(index, line[2])
        destinations[index] = line[2]
        index += 1

#   This function finds the id of the nearest location based on a given location id
def nearest(id, prev_id, ineligable):
    smallest = 100000000.0          # Sets the variable to a very large number so that basically everything will be smaller
    nearest_id = id                 # Sets the nearest id to the given id
    for i in range(27):             # Iterates through the number of destinations
        if distance_array[int(id)][i] != '':        # Checks the value on one side of the array
            distance = distance_array[id][i]
#            print(distance)
            if float(distance_array[id][i]) < smallest and float(distance_array[id][i]) != 0:   # if the value is smaller than smallest and is not 0
                if i not in prev_id and i not in ineligable:        # if the id is not in the visited set or ineligible set
                    smallest = float(distance_array[id][i])         # Then the smallest is updated to that value
                    nearest_id = i                                  # and the nearest is updated to that id
        elif distance_array[i][int(id)] != '':      # Checks the value in the other side of the array
            distance = distance_array[id][i]
#            print(distance)
            if float(distance_array[i][id]) < smallest and float(distance_array[i][id]) != 0:   # if the value is smaller than smallest and is not 0
                if i not in prev_id and i not in ineligable:        # if the id is not in the visited set or ineligible set
                    smallest = float(distance_array[i][id])         # Then the smallest is updated to that value
                    nearest_id = i                                  # and the nearest is updated to that id

#    print(smallest)
#    print(nearest_id)
    return nearest_id       # returns the id of the nearest location


#near = nearest(6)

#print(near)

#print(destinations[near])

#for _ in destination_array:
#    for i in _:
#        print(i, end=" ")
#    print()

#print(distance_array[24][1])