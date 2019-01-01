import mysql.connector
import os
from setupDB import mydb
from functions import addEmployee, mycursor, empData

try:
    colum = []
    for d in empData:
        colum.append(d)
    query = "CREATE TABLE employees ({0}{1})"
    mycursor.execute(query.format(' VARCHAR(255), '.join(colum), ' VARCHAR(255)'))
    mydb.commit()
except mysql.connector.errors.ProgrammingError as e:
    print(e)

try:
    os.system('cls')
except:
    os.system("clear")

print("Welcom to Smart Time Clock")
print("(c) 2018 HZA Solutions")
print("")

while True:
    cmd = input('{0}@{1}: {2}> '.format(mydb._user, mydb._host, mydb._database))
    if cmd == 'add':
        addEmployee()
    elif cmd == 'quit':
        break
    else:
        print("Invalid command...")