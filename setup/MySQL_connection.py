import mysql.connector
from RPLCD.i2c import CharLCD
import time

lcd = CharLCD('PCF8574', 0x27)

def setupDB(host, user, passwd, database):
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
        )
        lcd.clear()
        lcd.write_string('Connected to DB:')
        lcd.cursor_pos = (1,0)
        lcd.write_string('"%s"' % database)

        global Connection
        Connection = True
        return mydb
    except:
        try:
            mydb = mysql.connector.connect(
                host=host,
                user=user,
                passwd=passwd
            )
            mycursor = mydb.cursor()
            mycursor.execute('CREATE DATABASE %s' % database)

            lcd.clear()
            lcd.write_string("New DB created:")
            lcd.cursor_pos = (1,0)
            lcd.write_string('"%s"' % database)

            mydb.database = database
            time.sleep(2)
            lcd.clear()
            lcd.write_string('Connected to DB:')
            lcd.cursor_pos = (1,0) 
            lcd.write_string('"%s"' % database)

            Connection = True
            return mydb

        except:
            lcd.clear()
            lcd.write_string('Fail to connect,')
            lcd.cursor_pos = (1,0)
            lcd.write_string('user not found')
            time.sleep(2)

            Connection = False

print('')
print("Connecting to DB...")

while True:
    lcd.clear()
    lcd.write_string("Connecting to") 
    lcd.cursor_pos = (1,0)
    lcd.write_string('database...')
    print('')
    host = input("Host: ")
    user = input("User: ")
    passwd = input("Password: ")
    database = input("Database: ")

    mydb = setupDB(host, user, passwd, database)
    if Connection == True:
        time.sleep(2)
        lcd.clear()
        break