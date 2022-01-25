# Brian St. Germain    Student ID: 001509384
# Overall Big-O complexity  space: n^2, time:n^3

# importing csv file library
import csv
from Package import Package
from HashMap import HashMap
from Navigator import Navigator
from Truck import Truck

# these lists will store the csv values
distanceFields = []
distanceFieldsAddresses = []
distanceRows = []

packageFields = []
packageRows = []


# reading the distance csv file
with open("WGUPS Distance Table.csv", 'r') as file:  # space: n, time: n
    # creating an object to read the csv
    csvReader = csv.reader(file)

    # setting the fields
    distanceFields = next(csvReader)
    distanceFieldsAddresses = next(csvReader)

    # adding the rows
    for row in csvReader:
        distanceRows.append(row)


# reading the package csv file
with open("WGUPS Package File.csv", 'r') as file:  # space: n, time: n
    # creating an object to read the csv
    csvReader = csv.reader(file)

    # setting the fields
    packageFields = next(csvReader)

    # adding the rows
    for row in csvReader:
        packageRows.append(row)


# loading values into hash maps
distHashMap = HashMap()
packageHashMap = HashMap()  # hash map of Package objects

# loading distances into hash map
for values in distanceRows:  # space: n^2, time: n^2
    tempValuesList = []

    for pairs in values:
        tempValuesList.append(pairs)

    distHashMap.add(values[0], tempValuesList)


# loading packages into hash map
for index, packages in enumerate(packageRows):  # space: n, time: n
    tempPackage = Package(packages[0], packages[1], packages[2], packages[3], packages[4], packages[5], packages[7])
    packageHashMap.add(tempPackage.packageID, tempPackage)


# package IDs that each truck will be filled with
fillListTruckOne = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40, 2, 4, 5]
fillListTruckTwo = [3, 6, 18, 28, 32, 36, 38, 7, 8, 9, 10, 11, 12, 17, 21]
fillListTruckThree = [22, 23, 24, 26, 27, 33, 35, 39, 25]


truckOnePackages = []
truckTwoPackages = []
truckThreePackages = []

# uses the hash map to fill truck package lists
for value in fillListTruckOne:  # space: n, time: n
    truckOnePackages.append(packageHashMap.get(str(value)))

for value in fillListTruckTwo:  # space: n, time: n
    truckTwoPackages.append(packageHashMap.get(str(value)))

for value in fillListTruckThree:  # space: n, time: n
    truckThreePackages.append(packageHashMap.get(str(value)))


# create Truck objects and a Navigator object
time = Navigator(distanceRows, distanceFieldsAddresses)
truckOne = Truck(time.generateRoute(distanceRows[0], truckOnePackages), "Truck One")  # space: n, time: n^3
truckTwo = Truck(time.generateRoute(distanceRows[0], truckTwoPackages), "Truck Two")  # space: n, time: n^3
truckThree = Truck(time.generateRoute(distanceRows[0], truckThreePackages), "Truck Three")  # space: n, time: n^3


# generate the distances for each package
time.generateDistancesForPackages(truckOne)  # space: 1, time: n^2
time.generateDistancesForPackages(truckTwo)  # space: 1, time: n^2
time.generateDistancesForPackages(truckThree)  # space: 1, time: n^2


# CLI for the user to simulate package delivery. "exit" will exit the program. (x) where 'x' is an integer, will search a package. A lone integer will advance simulated minutes.
truckList = [truckOne, truckTwo, truckThree]
print("\nEnter 'exit' to exit")
print("To check package status, enter '(x)' . 'x' being the package ID")
print("To check all package statuses, enter 'check all'")
print("Package 0 is the HUB location\n")
userInput = ""
while userInput != "exit":  # space: 1, time: n^3
    print("Current time is: " + str(time.currentTime))
    userInput = input("Minutes to jump forward: ")

    # detects that a user is trying to look up a package
    if userInput[0] == '(' and userInput[len(userInput)-1] == ')':
        try:
            time.packageLookup(userInput, truckList)  # space: 1, time: n^2
        except:
            print("Incorrect lookup syntax")


    elif userInput == "check all":
        time.allPackageStatuses(truckList)

    elif userInput[0] == '-':
        print("Minutes may not be negative")

    # user isn't trying to look up a package, so call timeJump using the user's input
    else:
        try:
            int(userInput)
            time.timeJump(userInput, truckList)  # space: 1, time: n^3

        except:
            print("Minutes must be an integer")

    print()