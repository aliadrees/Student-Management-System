import json
def forgot():
    a=input("\nEnter Your Uername")

    try:
     with open('data.json','r') as f:
        users=json.load(f)
     for user in users:
       if user["username"]==a:
          password=input('Enter Your Passowrd')
          user["password"]=password
          break
     else:
         print("user Not found")
     with open('data.json','w') as f:
             json.dump(users,f,indent=4)
    except FileNotFoundError:
       print('File Not found')
    