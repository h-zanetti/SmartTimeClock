import mysql.connector
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

while True:
    print("To add an employee type 'add'")
    cmd = input()
    if cmd == 'add':
        addEmployee()
    elif cmd == 'quit':
        break
    else:
        print("Invalid command...")