try:
    import time
    import mysql.connector
    from RPLCD.i2c import CharLCD
except ImportError as e:
    print(e)

lcd = CharLCD('PCF8574', 0x27)

def err1049():
    global connection
    connection = False
    while connection == False:
        global mydb
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
        if str(e)[0:4] == "1049":
            print('Error #%s ' % e)
            connection = False
            print("It looks like the database '%s' does not exist," % db)
            print("To create such database type 'create'")
            print("To connect to another database type 'connect'")
            cmd = input()
            if str(cmd).lower() == "create":
                mydb = mysql.connector.connect(
                    host=host,
                    user=user,
                    passwd=passwd,
                    database=None
                )
                mycursor = mydb.cursor()
                mycursor.execute("CREATE DATABASE %s" % db)
                mydb.database = db
                for i in mycursor:
                    print(i)
                connection = True
            elif str(cmd).lower() == "connect":
                err1049()
        elif str(e)[0:4] == "1045":
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
                        if str(e)[0:4] == "1049":
                            err1049()
                else:
                    break
        else:
            print('Error #%s ' % e)
            connection = False
    except mysql.connector.errors.DatabaseError as e:
        if str(e)[0:4] == "2005":
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
                        break
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
    print("Fail to connect, do you want to try again? [Y/N]")
    cmd = input()
    if str(cmd).lower() == 'y':
        host = input("Host: ")
        user = input("User: ")
        psswd = input("Password: ")
        db = input("Database: ")
        connectDB(host, user, passwd, db)
    else:
        print("The system is not connected to a database,")
        print("Such connection must be created in order to use the system correctly.")
        break

if connection == True:
    lcd.clear()
    lcd.write_string("Successfully")
    lcd.cursor_pos = (1,0)
    lcd.write_string("connected to DB")
    time.sleep(3)
    lcd.clear()