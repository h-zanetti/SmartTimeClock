from setupDB import mydb
from functions import addEmployee, mycursor, empData

colum = []
for d in empData:
    colum.append(d)
query = "CREATE TABLE employees ({1}{2})"
mycursor.execute(query.format(' VARCHAR(255), '.join(colum), ' VARCHAR(255)'))
mydb.commit()

while True:
    cmd = input()
    if cmd == 'add':
        addEmployee()
    elif cmd == 'quit':
        break
    else:
        print("Invalid command...")