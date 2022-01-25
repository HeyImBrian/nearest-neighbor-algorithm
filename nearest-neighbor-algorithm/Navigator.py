import datetime
from Package import Package

class Navigator:
    def __init__(self, distanceRows, distanceFieldAddresses):
        self.randDate = datetime.date(2021, 12, 25)
        self.currentTime = datetime.datetime(2021, 12, 25, 8, 0)

        self.firstLeaveTime = datetime.datetime(2021, 12, 25, 8, 0)
        self.secondLeaveTime = datetime.datetime(2021, 12, 25, 9, 5)
        self.thirdLeaveTime = datetime.datetime(2021, 12, 25, 9, 55)

        self.distanceRows = distanceRows
        self.distanceFieldAddresses = distanceFieldAddresses

        self.deliveredPackages = []
        self.truckLaunchStatus = [False, False, False]



    # called by the CLI to advance input amount of minutes.
    def timeJump(self, inputMin, truckList):  # space: 1, time: n^3
        addTime = datetime.timedelta(minutes=1)

        for minute in range(int(inputMin)):
            self.checkTruckLaunch(truckList)  # space: 1, time: n^2
            self.currentTime += addTime

            # if a truck is active, the truck will move and check if it's at the right location to drop off a package
            for truck in truckList:
                if truck.active:
                    truck.moveTruck()

                    for index, package in enumerate(truck.packages):
                        if truck.currDistance >= package.distance:  # this is True when a package should be dropped off
                            package.timestamp = self.currentTime
                            print("From: " + truck.name + "     Dropped off package: " + str(package.packageID) + "     Time: " + str(package.timestamp) + "     Deadline: " + str(package.deadline) + "     Truck Mileage: " + str(package.distance) + "     Special Instructions: " + str(package.status))

                            package.currentLocationStatus = "Delivered"
                            self.deliveredPackages.append(package)
                            truck.packages.pop(index)



    # checks if the trucks are allowed to leave, makes them active if so
    def checkTruckLaunch(self, truckList):  # space: 1, time: n
        if self.currentTime >= self.firstLeaveTime and self.truckLaunchStatus[0] is False:
            truckList[0].active = True
            for package in truckList[0].packages:
                package.currentLocationStatus = "En route"

        if self.currentTime >= self.secondLeaveTime and self.truckLaunchStatus[1] is False:
            truckList[1].active = True
            for package in truckList[1].packages:
                package.currentLocationStatus = "En route"

        if self.currentTime >= self.thirdLeaveTime and self.truckLaunchStatus[2] is False:
            truckList[2].active = True
            for package in truckList[2].packages:
                package.currentLocationStatus = "En route"


    # prints the status of a certain package
    def packageLookup(self, input, truckList):  # space: 1, time: n^2
        id = input[1:len(input)-1]
        for package in self.deliveredPackages:
            if str(package.packageID) == str(id):
                print("This package is currently: " + package.currentLocationStatus)
                return None
        for truck in truckList:
            for package in truck.packages:
                if str(package.packageID) == str(id):
                    print("This package is currently: " + package.currentLocationStatus)
                    return None
        print("No package found")


    # prints all of the package's statuses
    def allPackageStatuses(self, truckList):  # space: 1, time: n^2
        for package in self.deliveredPackages:
            print("Package: " + package.packageID + "  Location: " + package.address + "    has been " + package.currentLocationStatus + "    " + str(package.timestamp))
        for truck in truckList:
            for package in truck.packages:
                print("Package: " + package.packageID + "  Location: " + package.address + "    has been " + package.currentLocationStatus + "    " + str(package.timestamp))


    # sets the distances for each package. Adds "HUB" locations, which represent the hub for distance purposes, and isn't an actual package
    def generateDistancesForPackages(self, truck):  # space: 1, time: n^2
        totalDistance = 0
        tempPackage = Package("0", "HUB", "", "", "", "", "Left the hub")
        tempPackage.distance = 0

        truck.packages.insert(0, tempPackage)  # insert the HUB to the beginning and end
        truck.packages.append(Package("0", "HUB", "", "", "", "", "Returned to hub"))

        for packageIndex in range(len(truck.packages) - 1):

            distanceRow = self.packageToDistanceRow(truck.packages[packageIndex])  # space: 1, time: n

            totalDistance += self.distBetween(distanceRow, truck.packages[packageIndex+1].address)  # space: 1, time: n
            truck.packages[packageIndex+1].distance = totalDistance  # set the package's distance to total distance



    # creates the route for each truck to deliver the packages. Uses the nearest neighbor algorithm
    def generateRoute(self, currentDistanceRow, packageList):  # space: n, time: n^3
        route = []

        currDistRow = currentDistanceRow
        remainingPackages = packageList

        for package in range(len(packageList)):
            closest = self.findClosest(currDistRow, remainingPackages)  # space: 1, time: n^2

            route.append(closest)
            currDistRow = self.packageToDistanceRow(closest)  # space: 1, time: n


        return route


    # given a package, returns the distance row that its located at
    def packageToDistanceRow(self, package):  # space: 1, time: n
        packageAddress = package.address

        for distRow in self.distanceRows:
            if distRow[1] == packageAddress:
                return distRow


    # uses the distBetween function to find the shortest distance of a list of packages
    def findClosest(self, currentDistanceRow, packageList):  # space: 1, time: n^2
        # first we must remove the current selected row
        for index, package in enumerate(packageList):
            if package.address == currentDistanceRow[1]:
                packageList.pop(index)
                break

        # then find the minimum distance
        minDist = packageList[0]
        minDistIndex = 0
        for index, package in enumerate(packageList):
            checkAgainstDist = self.distBetween(currentDistanceRow, package.address)  # space: 1, time: n
            checkMinDist = self.distBetween(currentDistanceRow, minDist.address)  # space: 1, time: n
            if checkAgainstDist < checkMinDist:
                minDist = package
                minDistIndex = index

        return minDist  # returns a package


    # finds the distance between two addresses
    def distBetween(self, currentDistanceRow, destinationAddress):  # space: 1, time: n
        # find index where fieldAddress matches the destinationAddress
        matchingFieldIndex = None
        for index, value in enumerate(self.distanceFieldAddresses):
            if value == destinationAddress:
                matchingFieldIndex = index
                break

        if matchingFieldIndex is None:
            return False

        # return the distance between the two locations
        distance = currentDistanceRow[matchingFieldIndex + 2]
        return float(distance)