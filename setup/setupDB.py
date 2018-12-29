import mysql.connector
''' 
def err1049()
def err1045()
def err2005()
'''

def connectDB(host, user, passwd, db):
    try:
        global mydb
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=db
        )
        global connection
        connection = True
    except mysql.connector.errors.ProgrammingError as e:
        if str(e) == "1049 (42000): Unknown database '%s'" % db:
            print('Error #%s ' % e)
            connection = False
            while connection == False:
                mydb = mysql.connector.connect(
                    host=host,
                    user=user,
                    passwd=passwd,
                )
                print("Try connect to another database:")
                cmd = input()
                if cmd != 'quit':
                    try:
                        mydb.database = str(cmd)
                        connection = True
                    except mysql.connector.errors.ProgrammingError as e:
                        print('Error #%s ' % e)
                        connection = False
                else:
                    break
        elif str(e) == "1045 (28000): Access denied for user '%s'@'%s' (using password: YES)" % (user, host):
            print('Error #%s ' % e)
            connection = False
            while connection == False:
                print("Try login with a different user:")
                usr = input("Username: ")
                if usr != 'quit':
                    pwd = input("Password: ")
                    try:
                        mydb = mysql.connector.connect(
                            host=host,
                            user=str(usr),
                            passwd=str(pwd),
                            database=db
                        )
                        connection = True
                    except mysql.connector.errors.ProgrammingError as e:
                        print('Error #%s ' % e)
                        connection = False
                        if str(e)[0:4] != "1045":
                            break
                else:
                    break
        else:
            print('Error #%s ' % e)
            connection = False
    except mysql.connector.errors.DatabaseError as e:
        if str(e) == "2005 (HY000): Unknown MySQL server host '%s' (0)" % host:
            print('Error #%s ' % e)
            connection = False
            while connection == False:
                print("Try connect to a different host:")
                cmd = input()
                if cmd != 'quit':
                    try:
                        mydb = mysql.connector.connect(
                            host=str(cmd),
                            user=user,
                            passwd=passwd,
                            database=db
                        )
                        connection = True
                    except mysql.connector.errors.ProgrammingError as e:
                        print('Error #%s ' % e)
                        connection = False
                        break
                    except mysql.connector.errors.DatabaseError as e:
                        print('Error #%s ' % e)
                        connection = False
                else:
                    break
        else:
            print('Error #%s ' % e)
            connection = False

host = input("Host: ")
user = input("User: ")
passwd = input("Password: ")
db = input("Database: ")
connectDB(host, user, passwd, db)

while connection == False:
    print("Fail to connect, do you ant to try again? [Y/N]")
    cmd = input()
    if str(cmd).lower() == 'y':
        host = input("Host: ")
        user = input("User: ")
        psswd = input("Password: ")
        db = input("Database: ")
        connectDB(host, user, passwd, db)
    else:
        break