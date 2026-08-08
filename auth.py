# Login module
import json
def login():
 
 username=input("Enter your username:")

 password=input("\nEnter your password:")
 try:
   
  with open("data.json", "r") as f:
    users = json.load(f)
 

    for user in users:
        if user["username"] == username and user["password"] == password:
            print("User login Successful!")
            return True

    print("User not login!")
    return False
 except FileNotFoundError:
       print("File Not found!")
import json

def sigin():

    name = input("Enter Your First Name: ")
    fathername = input("Enter Your Father Name: ")

    while True:
        email = input("Enter your Email: ")

        if '@' in email and '.' in email:
            print("Valid email!")
            break
        else:
            print("Your Email is invalid!")

    while True:
        password = input("Enter Your Password (minimum 8 characters): ")
        password2 = input("Re-enter Your Password: ")

        if len(password) < 8:
            print("Password must contain at least 8 characters!")
            continue

        if password != password2:
            print("Your passwords do not match!")
            continue

        print("Your Password is valid and matched!")
        break

    user = {
        "name": name,
        "fathername": fathername,
        "password": password,
        "username": email
    }

    try:
        with open("data.json", "r") as f:
            users = json.load(f)

    except (FileNotFoundError, json.JSONDecodeError):
        users = []

    users.append(user)

    print("\nUser that will be saved:")
    print(user)

    print("\nTotal users:", len(users))

    with open("data.json", "w") as f:
        json.dump(users, f, indent=4)

    print("\nSaved successfully!")