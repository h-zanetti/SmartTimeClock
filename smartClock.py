import mysql.connector
import datetime

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="frida14&IPA17",
    database="SmartTimeClock"
)
mycursor = mydb.cursor()

data = ('id', 'name', 'fingerprint_1', 'fingerprint_2', 'salary')

def addEmployee():
    employeeData = {}
    for d in data:
        info = input("%s: " % d)
        collectedData = {d : info}
        employeeData.update(collectedData)
    col = []
    val = []
    for key in employeeData:
        col.append(key)
        val.append(employeeData[key])
    sql = "INSERT INTO employees ({0}) VALUES ({1})"
    mycursor.execute(sql.format(', '.join(col), ', '.join( repr(e) for e in val)))
    mydb.commit()
