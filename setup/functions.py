import setupDB
import datetime

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

def dateTime():
    dt = str(datetime.datetime.now())
    date = dt[0:10]
    time = dt[11:16]
    dateTime = [date, time]
    return dateTime

def getHours(ID):
    info = getInfo(ID)
    if info != None:
        name = info[1]
        dt = dateTime()
        total = 0
        query = "SELECT * FROM {0} WHERE date = '{1}'"
        mycursor.execute(query.format(name.lower(), dt[0]))
        rows = mycursor.fetchall()
        for row in rows:
            if row[2] != None:
                Hrs = int(row[2][0:2]) - int(row[1][0:2])
                Min = (60 - int(row[1][3:5]) + int(row[2][3:5]))/60
                if Hrs == 0:
                    Min = (int(row[2][3:5]) - int(row[1][3:5]))/60
                    total = Min
                elif Hrs == 1:
                    total = Min
                else:
                    total = Hrs + Min
        query = "UPDATE {0} SET hours = {1} WHERE hours is NULL"
        mycursor.execute(query.format(name.lower(), round(total, 2)))
    else:
        lcd.clear()
        lcd.write_string("invalid identification.")

    mydb.commit()

def totalHours(ID):
    info = getInfo(ID)
    if info != None:
        name = info[1]
        query = "SELECT * FROM {0}"
        mycursor.execute(query.format(name))
        rows = mycursor.fetchall()
        total = 0
        for row in rows:
            total += float(row[3])
            query = "UPDATE {0} SET total_hours = {1} WHERE clock_out = '{2}'"
            mycursor.execute(query.format(name.lower(), total, row[2]))
    else:
        lcd.clear()
        lcd.write_string("invalid identification.")

    mydb.commit()

def clock_in(ID):
    info = getInfo(ID)
    if info != None:
        name = info[1]
        lcd.clear()
        lcd.write_string('Welcome back,')
        lcd.cursor_pos = (1,0)
        lcd.write_string(info[2]) # Greets employee by the first name
        confirmation = "Are you clocking in? [Y/N] "
        cmd = input(confirmation)
        if cmd.lower() == 'y':
            dt = dateTime()

            query = "INSERT INTO {0} (date, clock_in) VALUES ('{1}', '{2}')"
            mycursor.execute(query.format(name.lower(), dt[0], dt[1]))
    else:
        lcd.clear()
        lcd.write_string("invalid identification.")

    mydb.commit()

def clock_out(ID):
    info = getInfo(ID)
    if info != None:
        name = info[1]
        dt = dateTime()
        query = "SELECT * FROM {0} WHERE date = '{1}'"
        mycursor.execute(query.format(name.lower(), dt[0]))
        rows = mycursor.fetchall()
        for row in rows:
            if row != None and row[2] == None:
                confirmation = input("{0}, are you clocking out? [Y/N] ".format(info[2]))
                if confirmation.lower() == 'y':
                    dt = dateTime()
                    query = "UPDATE {0} SET clock_out = '{1}' WHERE clock_out is NULL"
                    mycursor.execute(query.format(name.lower(), dt[1]))
        getHours(ID)
        totalHours(ID)
        print("You are off the clock.")
    else:
        lcd.clear()
        lcd.write_string("invalid identification.")

    mydb.commit()

def getPaychecks(date):
    table = "paychecks_%s" % date
    query = "CREATE TABLE {0} (id VARCHAR(255), name VARCHAR(255), hours VARCHAR(255), salary VARCHAR(255), paycheck VARCHAR(255))"
    mycursor.execute(query.format(table))

    mycursor.execute("SELECT * FROM employees")
    rows = mycursor.fetchall()
    for row in rows:
        info = getInfo(row[0])
        query = "INSERT INTO {0} (id, name, salary) VALUES ('{1}', '{2}', '{3}')"
        mycursor.execute(query.format(table, info[0], info[1], info[-1]))
        mydb.commit()
        
        query = "SELECT * FROM {0}"
        mycursor.execute(query.format(info[1].lower()))
        rows1 = mycursor.fetchall()
        totalHours = rows1[-1][-1]
        query = "UPDATE {0} SET hours = {1} WHERE id = {2}"
        mycursor.execute(query.format(table, totalHours, info[0]))
        mydb.commit()

        paycheck = float(totalHours) * float(info[-1])
        query = "UPDATE {0} SET paycheck = {1} WHERE id = {2}"
        mycursor.execute(query.format(table, paycheck, info[0]))
        mydb.commit()
