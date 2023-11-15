import sqlite3
import hashlib

print("Welcome to Hashing Programm of MD5 in python")

while True:
    print("(R)egister, (L)ogin, (S)how Data, (Q)uit")
    inputChoice = input("")
    if inputChoice not in ['R','r','L','l', 'S','s','Q','q']:
        print("Invalid Input")
        continue
    else:
        conn = sqlite3.connect('userdata.db')
        if inputChoice in ['R','r']:
            counter = 0
            userName = input("User Name           :")
            userPassword = input("Password           :")
            MD5_Hashed_Object = hashlib.md5(userPassword.encode())
            Hashed_String_Hex = MD5_Hashed_Object.hexdigest()
            conn.execute("""CREATE TABLE IF NOT EXISTS USERDATA 
            (ID INT, USER_NAME TEXT NOT NULL, PASSWORD TEXT NOT NULL, HASHEDPASS TEXT NOT NULL)""")
            dataTale = conn.execute("SELECT * FROM USERDATA")
            for row in dataTale:
                counter += 1
            conn.execute("INSERT INTO USERDATA (ID,USER_NAME,PASSWORD,HASHEDPASS) VALUES (?,?,?,?)",(counter+1, userName, userPassword,Hashed_String_Hex))
            print("Registration successfully done.")
            conn.commit()
            conn.close()

        elif inputChoice in ['L','l']:
            inputUserName = input("User Name            :")
            inputPassword = input("Password            :")
            inputHashedPasswordObj = hashlib.md5(inputPassword.encode())
            inputHashedPasswordStr = inputHashedPasswordObj.hexdigest()
            DataInTale = conn.execute("SELECT * FROM USERDATA")
            if DataInTale == None:
                print("Please Register an account first")
            else:
                for row in DataInTale:
                    if inputUserName == row[1]:
                        if inputHashedPasswordStr == row[3]:
                            print("Welcome, You Logged in Successfully")
                            break
                else:
                    print("User Name or Password is incorrect.")
            conn.close()
        elif inputChoice in ['S','s']:
            DataInTale = conn.execute("SELECT * FROM USERDATA")
            print("ID             Name                    Password                       Hashed Password")
            for row in DataInTale:
                print(str(row[0])+ "              "+row[1]+"                    "+row[2]+"                       "+row[3])
            conn.close()
        elif inputChoice in ['Q','q']:
            print("Thanks for using this script")
            break
        else:
            print("Invalid Command")

