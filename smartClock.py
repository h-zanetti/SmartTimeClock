import mysql.connector
import datetime

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="frida14&IPA17",
    database="SmartTimeClock"
)
mycursor = mydb.cursor()

empData = ['id', 'last_name', 'first_name', 'fingerprint_1', 'fingerprint_2', 'salary']
empTable = ['date', 'clock_in', 'clock_out', 'hours', 'total_hours',]

def addEmployee():
    employeeData = {}
    for d in empData:
        info = input("%s: " % d)
        collectedData = {d : info}
        employeeData.update(collectedData)
    
    col = []
    val = []
    for key in employeeData:
        col.append(key)
        val.append(employeeData[key])
    cmd = "INSERT INTO employees ({0}) VALUES ({1})"
    mycursor.execute(cmd.format(', '.join(col), str(val)[1:-1]))

    name = employeeData["last_name"]
    col = []
    for d in empTable:
        col.append(d)
    cmd = "CREATE TABLE {0} ({1}{2})"
    mycursor.execute(cmd.format(name.lower(), ' VARCHAR(255), '.join(col), ' VARCHAR(255)'))

    mydb.commit()

# Always that 'name' is refering to the employee, it is his/her last name

def removeEmployee(name): 
    remove = "DELETE FROM employees WHERE last_name = '{0}'"
    mycursor.execute(remove.format(name))
    delete = "DROP TABLE {0}"
    mycursor.execute(delete.format(name.lower()))

    mydb.commit()

def getInfo(ID):
    query = "SELECT * FROM employees WHERE id = {0}"
    mycursor.execute(query.format(ID))
    row = mycursor.fetchone()
    info = []
    if row != None:
        for i in row:
            info.append(i)
        return info
    else:
        return None

def clock_in(ID):
    info = getInfo(ID)
    if info != None:
        name = info[1]
        print("Welcome back, {0}.".format(info[2])) # Greets employee by the first name
        confirmation = input("Are you clocking in? [Y/N] ")
        if confirmation.lower() == 'y':
            dateTime = str(datetime.datetime.now())
            date = dateTime[0:10]
            time = dateTime[11:16]
            query = "INSERT INTO {0} (date, clock_in) VALUES ('{1}', '{2}')"
            mycursor.execute(query.format(name.lower(), date, time))
    else:
        print("Invalid identification, make sure you are registered on the system and try again.")

    mydb.commit()

def clock_out(ID):
    info = getInfo(ID)
    if info != None:
        name = info[1]
        date = str(datetime.datetime.now())[0:10]
        query = "SELECT * FROM {0} WHERE date = '{1}'"
        mycursor.execute(query.format(name, date))
        row = mycursor.fetchone()
        if row != None and row[2] == None:
            confirmation = input("{0}, are you clocking out? [Y/N] ".format(info[2]))
            if confirmation.lower() == 'y':
                dateTime = str(datetime.datetime.now())
                time = dateTime[11:16]
                query = "UPDATE {0} SET clock_out = '{1}' WHERE date = '{2}'"
                mycursor.execute(query.format(name.lower(), time, date))
        else:
            clock_in(ID)
    else:
        print("Invalid identification, make sure you are registered on the system and try again.")

    mydb.commit()
