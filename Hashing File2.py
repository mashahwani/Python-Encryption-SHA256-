from flask import (Flask, render_template, request, redirect, url_for, )
import uuid
import hashlib



def Hash_My(Password):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + Password.encode()).hexdigest() + ':' + salt


def Compare_These( HashedPassword, UserPassword):
    password, salt = HashedPassword.split(':')
    return password == hashlib.sha256(salt.encode() + UserPassword.encode()).hexdigest()

app = Flask(__name__)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        position = 0
        UserNamesDataFile = open("Users", "r")
        UserPasswordsDataFile = open("UsersPasswords", "r")
        UserName = request.form["name"]
        UserPassword = request.form["password"]
        for Name in UserNamesDataFile:

            if Name[:-1] == UserName:
                for counter in range(position+1):
                    Hashed_Password = UserPasswordsDataFile.readline()
                    if counter == position:
                        if Compare_These(Hashed_Password[:-1],UserPassword):
                            UserNamesDataFile.close()
                            UserPasswordsDataFile.close()
                            return render_template("Welcome Page.html", Name = UserName, Password = UserPassword, HPassword = Hashed_Password)
                else:
                    UserNamesDataFile.close()
                    UserPasswordsDataFile.close()
                    return "<h1> Email or Password is incorrect </h1>"
            position += 1

        else:
            UserNamesDataFile.close()
            UserPasswordsDataFile.close()
            return "<h1> Account Doesn't Exist </h1>"


    else:
        return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        UserNames = open("Users", 'a')
        UserPasswords = open("UsersPasswords", "a")
        UserName = request.form["email"]
        UserPassword = request.form["password"]
        UserNames.write(UserName + "\n")
        UserPasswords.write(Hash_My(UserPassword) + "\n")
        UserPasswords.close()
        UserNames.close()
        return "<h1>Registered Succesfully<h1>"
    else:
        return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)