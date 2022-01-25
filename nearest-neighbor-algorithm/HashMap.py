class HashMap:
    def __init__(self):
        self.size = 27
        self.map = [None] * self.size


    # converts a key to a hash value
    def getHash(self, key):  # space: 1, time: n
        hash = 0
        for char in key:
            hash += ord(char) % 10

        hash %= 27
        return hash


    # adds or updates a given object using the given key
    def add(self, key, value):  # space: 1, time: n
        hash = self.getHash(key)
        keyValuePair = [key, value]

        if self.map[hash] is None:  # if nothing is found at the hash location:
            self.map[hash] = list([keyValuePair])  # make that location equal the keyValuePair
            return True

        for pairValues in self.map[hash]:  # There is at least one value at the hash location, so cycle through them
            if pairValues[0] == key:  # if two items have the same key:
                pairValues[1] = value  # update the stored value
                return True

        self.map[hash].append(keyValuePair)  # this key is unique, so append the keyValuePair to the map
        return True


    # gets an object with the given key
    def get(self, key):  # space: 1, time: n
        hash = self.getHash(key)

        if self.map[hash] is not None:  # if values are at the asked location:
            for pairValues in self.map[hash]:  # iterate through all the values at the location
                if pairValues[0] == key:  # if a key matches the input key:
                    return pairValues[1]  # return the corresponding value
        return None