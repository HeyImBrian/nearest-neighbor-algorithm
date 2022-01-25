
class Package:
    def __init__(self, packageID, address, city, state, zip, deadline, status):
        self.packageID = packageID
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip = zip
        #self. weight = weight
        self.status = status
        self.currentLocationStatus = "At the hub"
        self.distance = None
        self. timestamp = ""