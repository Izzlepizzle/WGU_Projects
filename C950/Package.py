# Package class file
# In this file I have the package and hashtable class.
# I have them in the same file to avoid circular importing since they both rely heavily on each other.

import csv


class HashTable:
    def __init__(self):
        self.size = 40
        self.hashmap = [[] for _ in range(0, self.size)]

    # This creates a key for each bucket in the hash table
    # I didn't use the built in hash() function because I know exactly how many packages there will be and wanted them in their own buckets.
    def hashing(self, key):
        return key % self.size

    # This function sets the value in each bucket given a key value.
    # It creates a package object that will be entered as the value of the bucket.
    # This function also accounts for chaining with each bucket.
    def set(self, key, address, deadline, city, zip, weight, special, status, p_id):
        p = Package(key, address, deadline, city, zip, weight, special, status, p_id)
        hashKey = self.hashing(key)
        bucket = self.hashmap[hashKey]
        index = 0
        keyExists = False
        for i, kv in enumerate(bucket):
            k, v = kv
            index = i
            if key == k:
                keyExists = True
                break

        if keyExists:
            bucket[index] = (key, p)

        else:
            bucket.append((key, p))

    # This method returns a value from the hash table given a key.
    # It also accounts for chaining.
    def get(self, key):
        hashKey = self.hashing(key)
        bucket = self.hashmap[hashKey]
        for kv in bucket:
            k, v = kv
            if key == k:
                return v
            else:
                print(key)
                raise KeyError('Item not found')

    # This method can change the value of the status of a particular package object
    def set_status(self, key, status):
        hashKey = self.hashing(key)
        bucket = self.hashmap[hashKey]

        for kv in bucket:
            k, v = kv
            if key == k:
                v.status = status
            else:
                raise KeyError('Item not found')

    # This method can change the address value of a particular package object
    def set_address(self, key, address, p_id):
        hashKey = self.hashing(key)
        bucket = self.hashmap[hashKey]

        for kv in bucket:
            k, v = kv
            if key == k:
                v.address = address
                v.p_id = p_id
            else:
                raise KeyError('Item not found')


class Package:
    def __init__(self, id, address, deadline, city, zip, weight, special, status, p_id):
        self.id = id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip = zip
        self.weight = weight
        self.status = status
        self.special = special
        self.p_id = p_id

# Here we actually create the hashtable
hashTab = HashTable()

# And here we load the csv file into our hashtable directly
with open('Packages.csv', encoding="utf-8-sig") as csvFile:
    csvReader = csv.reader(csvFile)

    for line in csvReader:
        p = Package(int(line[0]), line[1], line[5], line[2], line[4], line[6], line[7], 'Depot', int(line[8]))
        #print(p.id)
        hashTab.set(p.id, p.address, p.deadline, p.city, p.zip, p.weight, p.special, p.status, p.p_id)




#print(hashTab.hashmap)
#p = hashTab.get(7)
#print(p.status)
#print(hashTab.get(7))
#hashTab.set_status(7, "Delivered")
#p = hashTab.get(7)
#print(hashTab.get(7))
#print(p.status)



