import mysql.connector

try:
    mydb = mysql.connector.connect(
        host='localhost', #DatabaseError: 2005
        user='root', #ProgramingError: 1045
        passwd='frida14&IPA17', #ProgramingError: 1045
        database='smarttimeclock' #ProgramingError: 1049
    )
except mysql.connector.errors.ProgrammingError as e:
    print(e)
    mydb = mysql.connector.connect(
        host='localhost', #DatabaseError: 2005
        user='root', #ProgramingError: 1045
        passwd='frida14&IPA17', #ProgramingError: 1045
    )
    mydb.database = "world"
    msg = "Connected to database '{0}' as '{1}'@'{2}' [PASSWORD: '{3}']"
    print(msg.format(mydb.database, mydb._user, mydb._host, mydb._password))