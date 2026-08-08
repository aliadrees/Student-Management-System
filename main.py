from pathlib import Path
Path("data").mkdir(exist_ok=True)
from auth import sigin,login
from forgot import forgot
from StudentManager import StudentManager
while True:
   s1=StudentManager()
   print("\n1----Login(1--admin,2--user)")
   print("\n3----Sign in")
   print("\n4----forgot Password")
   print("\n5-----Exit")
   a=int(input("Select any one from the following Four options:"))
   if a==2:
     
     if login():
          print("Login Successfully!")
          print("Welcome to the Student Management System")
          while True:
             print("--------------------------------")
             
             print("\n1----View Student")
             print("\n2----Update Student")
             print("\n3----Search Student")
             print("\n4----Exit")
             print ("\n--------------------------------")
             b=int(input("Select any one from the following Four options:"))
             if b==1:
                s1.viewStudent()
             elif b==2:
                  s1.updateStudent()
             elif b==3:
                  s1.searchStudent()
             elif b==4:
                  print('Thank You very much. You are going to exit')
                  break
   elif a==1:
      s2=StudentManager()
      username=input("Enter your username:")
      password=input("\nEnter your password:")
      if username=="admin" and password=="admin":
              print("Admin login Successful!")
              print("Welcome to the Student Management System")
              while True:
                 print("--------------------------------")
                 print("\n1----Add Student")
                 print("\n2----View Student")
                 print("\n3----Update Student")
                 print("\n4----Search Student")
                 print("\n5----department wise student")
                 print("\n6----semester wise student")
                 print("\n7-----higest cgpa student")
                 print("\n8-----lowest cgpa student")
                 print("\n9----Convert Student data to CSV")
                 print("\n10----Exit")
                 print ("\n--------------------------------")
                 b=int(input("Select any one from the following Five options:"))
                 if b==1:
                    s2.add_Student()
                 elif b==2:
                    s2.viewStudent()
                 elif b==3:
                      s2.updateStudent()
                 elif b==4:
                      s2.searchStudent()
                 elif b==5:
                      s2.departmentsearch()
                 elif b==6:
                        s2.semestersearch()
                 elif b==7:
                        s2.Higestcgpa()
                 elif b==8:
                        s2.lowestcgpa()
                 elif b==9:
                        s2.export_to_csv()
                 elif b==10:
                      print('Thank You very much. You are going to exit')
                      break
      else:
              print("Admin not login!")
   elif a==3:
      sigin()
   elif a==4:
      forgot()
   elif a==5:
      print('Thank You very much. You are going to exit')
      break
      


main()
