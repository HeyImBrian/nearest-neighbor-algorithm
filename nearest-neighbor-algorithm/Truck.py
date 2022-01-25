
class Truck:
    def __init__(self, packages, name):
        self.name = name
        self.active = False  # gets set to active when the truck leaves the bay
        self.packages = packages
        self.location = "HUB"
        self.destination = None
        self.currDistance = 0
        self.speed = 0.3  # per minute


    # moves the truck 0.3 miles. Called once per minute because the truck moves at 18 miles per hour
    def moveTruck(self):  # space: 1, time: 1
        self.currDistance += 0.3

