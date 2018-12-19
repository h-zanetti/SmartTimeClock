import datetime

data = ['ID', 'Name', 'Finger Print #1', 'Finger Print #2', 'ClockIn', 'ClockOut', 'Hours', 'TotalHours', 'Paycheck']

inputs = ['ID', 'Finger Print #1', 'Finger Print #2']
outputs = ['Name', 'Hours', 'TotalHours', 'Paycheck']

dataBase = {}

def addEmployee(name):
        employeeData = {}
        for d in data:
                info = input("%s: " % d)
                collectedData = { d : info}
                employeeData.update(collectedData)
                person = {name : employeeData}
        dataBase.update(person)

def removeEmployee(name):
        dataBase.pop(name)

def generateDB():
        ID = 0
        employees = ['Henrique', 'Jahjir', 'Justin', 'Al', 'Jessica', 'Seanna', 'Lindsey', 'Michael', 'Gail']

        for emp in employees:
                emp = {}
                ID += 1
                for d in data:
                        dataCollected = {d : None}
                        emp.update(dataCollected)
                emp["ID"] = ID
                emp["Name"] = employees[ID]
                emp["Finger Print #1"] = (ID + 1) * 578532
                emp["Finger Print #2"] = (ID + 1) * 235875
                emp["Hours"] = {}
                emp["ClockIn"] = []
                emp["ClockOut"] = []
                emp["TotalHours"] = 0
                emp["Paycheck"] = 0
                newEmployee = {emp["Name"] : emp}
                dataBase.update(newEmployee)

def getHours(name):
        clockIn = dataBase[name]["ClockIn"]
        clockOut = dataBase[name]["ClockOut"]
        Hours = dataBase[name]["Hours"]
        dateTime = str(datetime.datetime.now())
        Hrs = 0
        Min = 0
        for i in clockIn:
                i=0
                Hrs = int(clockOut[i][11:13]) - int(clockIn[i][11:13])
                Min = (59 - int(clockIn[i][14:16])) + int(clockOut[i][14:16]) / 60
                total = Hrs + Min
                newHour = {dateTime[5:10] : total}
                Hours.update(newHour)
                i += 1
        if dateTime[5:10] in Hours:
                return Hours[dateTime[5:10]]
        else:
                return "You didn't work today"

def getTotalHours(name):
        hrs = dataBase[name]["Hours"]
        totalHours = sum(hrs.values())
        dataBase[name]["TotalHours"] = totalHours
        return totalHours

def clockIn(name):
        print(" %s, are you clocking in?" % name)
        confirmation = input("(Y/N) ")
        if confirmation.lower() == 'y':
                dateTime = str(datetime.datetime.now())
                dataBase[name]["ClockIn"].append(dateTime)
                print("Welcome back! You are ready to go.")
        else:
                return confirmation

def clockOut(name):
        print("%s, are you clocking out?" % name)
        confirmation = input("(Y/N) ")
        if confirmation.lower() == 'y':
                dateTime = str(datetime.datetime.now())
                dataBase[name]["ClockOut"].append(dateTime)
                print("See you soon, %s" % name)
                getHours(name)
                print('Worked today: %s' % dataBase[name]["Hours"][dateTime[5:10]])
                getTotalHours(name)
                print('Worked this month: %s' % dataBase[name]["TotalHours"])
        else:
                return confirmation

def getPaycheck(name, perHour):
        base = dataBase[name]
        getHours(name)
        getTotalHours(name)
        paycheck = base["TotalHours"] * perHour
        base["Paycheck"] = paycheck
        return paycheck

generateDB()

print("Welcom to Smart Clock")
print("(c) 2018 HZA Solutions")
print(' ')

me = "Henrique"
base = dataBase[me]
mineHours = {'12-03' : 4, '12-04' : 4.5, '12-05' : 3.75, '12-06' : 4, '12-07' : 2}
base["Hours"].update(mineHours)

tries = 0
while (tries < 3):
        username = input("Username: ")
        ID = input("ID: ")
        if username in dataBase and int(ID) == dataBase[username]["ID"]:
                print("Hello, %s!" % username)
                while(True):
                        firstCall = input()
                        lower = firstCall.lower()
                        if lower == "add employee":
                                print("What is the name of your employee?")
                                name = input()
                                addEmployee(name)
                        elif lower == "remove employee":
                                print("Please, type the name of the employee that you wish to be removed:")
                                name = input()
                                removeEmployee(name)
                        elif lower == "clock in":
                                print(clockIn(username))
                        elif lower == "clock out":
                                print(clockOut(username))
                        elif lower == "my hours":
                                print(getHours(username))
                        elif lower == "my total hours":
                                print(getTotalHours(username))
                        elif lower == "my paycheck":
                                print(getPaycheck(username, 10))
                        elif lower == "get hours":
                                print("Please, type the employee's name that you wish to check the list of dates and amaount of hours worked")
                                print("Or '*' to select all employees")
                                name = input()
                                if name == "*":
                                        for employee in dataBase:
                                                getHours(employee)
                                                print("%s: " % dataBase[employee]["Name"])
                                                print("    %s" % dataBase[employee]["Hours"])  # Check how to make this a table of dates and hours worked
                                else:
                                        getHours(name)
                                        print(dataBase[name]["Hours"])
                        elif lower == "get total hours":
                                print("Please, type the employee's name that you wish to check the total amount of hours worked this month:")
                                print("Or '*' to select all employees")
                                name = input()
                                if name == "*":
                                        for employee in dataBase:
                                                getTotalHours(employee)
                                                print("{0}: {1}".format(dataBase[employee]["Name"], dataBase[employee]["TotalHours"]))
                                else:
                                        getTotalHours(name)
                                        print(dataBase[name]["TotalHours"])
                        elif lower == "get paychecks":
                                print("Please, type the employee's name that you wish to check the paycheck:")
                                print("Or '*' to select all employees")
                                name = input()
                                if name == "*":
                                        for employee in dataBase:
                                                getPaycheck(employee, 10)
                                                print("{0}: ${1}".format(dataBase[employee]["Name"], dataBase[employee]["Paycheck"]))
                                else:
                                        getPaycheck(name, 10)
                                        print('$%s' % dataBase[name]["Paycheck"])
                        elif lower == "quit":
                                break
                        else:
                                print("Command not found")
                break
        else:
                print("Invalid username or ID, try again")
                tries += 1
else:
        print("Due to security issues, the system is temporarily blocked.")