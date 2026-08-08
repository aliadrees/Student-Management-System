import Student
import json
import os
import csv

print(os.getcwd())
from Student import Student
class StudentManager:
    def add_Student(self):
        while True:
         name=input("\nEnter Your Full Name(Must be in Latters)")
        
         if name.replace(" ","").isalpha():
            print("\nYour Name is Valid!")
            break
         else:
            print("\nRe-Enter Your Name!")
        while True:
             fathername=input("\nEnter Your Father Name(Must be in Latters)")
                   
             if fathername.replace(" ","").isalpha():
                       print("\nFather Name is Valid!")
                       break
             else:
                       print("\nRe-Enter Your Name!")
        while True:
             try:
                  age=int(input("\nEnter Your Age"))
                  if age in range(15,61):
                       print("\nYour are Eligible")
                       break
                  else:
                       print('\nYou are not eligible to apply')
                       a=int(input(("\nif you want to back home than press 0")))
                       if a==0:
                            return
             except ValueError:
                    print("\nPlease Enter the input in integer")
                    n=int(input("\nif you want to go back than press 1"))
                    if n==1:
                         return
        while True:
               ggen1=("Male",'Female','Other')
               gen=input("\nEnter your Gender(Male,Femal,other)")
               if gen in ggen1:
                     
                    break
          
               else:
                    print("\nplease Enter the following giving options(Male,Femal,other)")
        while True:
               dep1=("Software Engineering",'Computer Science',"Artifical Inteligence","Computer Engineering") 
               dep=input("Please Enter Your Depatrtment")
               if dep in dep1:
                    break
               else:
                    print("\nplease Enter your department in the following options"
                    "(Software Engineering,Computer Science,Artifical Inteligence,Computer Engineering)")
        while True:
               try:
                    n=float(input("\nEnter Your Cgpa (must in 0.0-4.0)"))
                    if 0.0 <= n <= 4.0:
                         break
                    else:
                         print("\nplease Enter your Cgpa (must in 0.0-4.0) ")
                         n=int(input("\nif you want to go back than press 1"))
                         if n==1:
                               return
               except ValueError:
                    print("\nPlease enter your value in Float")
        while True:
             email=input("Enter your Email(Your Email must in @format):")
             if '@' in email and '.' in email:
                      print("Valid email! ")
                      break
             else:
                      print("Your Email is invalid!")
        while True:
               phone=input("Enter Your Phone No")
               try:
                                   phone=(input("\nEnter Your phone no (must in 11 Digit)"))
                                   if phone.isdigit() and len(phone)==11:
                                        break
                                   else:
                                        print("\nplease Enter your phone (must in 11 digit) ")
                                        n=int(input("\nif you want to go back than press 1"))
                                        if n==1:
                                              return
               except ValueError:
                                   print("\nPlease enter your value in Float")
        while True:
               sem=int(input("\nPlease Enter Your Semester"))
               semester=(1,2,3,4,5,6,7,8)

                       
               if sem in semester:
                     break
               else:
                     print("\nPlease Re_enter Your Semester!")

        s1=Student(name,fathername,age,gen,dep,sem,n,phone,email)
        r=s1.to_dic()
        s1.save(r)
        print("Congratulation Your information is submit")
    def viewStudent(self):
          try:
                id=int(input("\nEnter your Student id:"))
                with open("Student.json","r")as f:
                      Students=json.load(f)
                      for student in Students:
                            if student["student_id"]==id:
                                    print("\n----------------")
                                    print("\nID:", student["student_id"])
                                    print("\nName:", student["student_name"])
                                    print("\nDepartment:", student["department"])
                                    print("\nFather Name:",student["father_name"])
                                    print("\nCurrent Semester",student["semester"])
                                    print("\nCurrent CGPA",student["cgpa"])
                                    print("\n----------------")

          except FileNotFoundError:
                print("\nFile Not Found")
    def  searchStudent(self):
          id=int(input("\nEnter the Student Which you want to found:")) 
          try:
                with open("Student.json","r") as f:
                      students=json.load(f)
                      
                      for student  in students:
                            if student["student_id"]==id:
                                  print("\n------------------")  
                                  print("\nFound: ",student["student_id"])
                                  print("\nStudent Name : ",student["student_name"])  
                                  print("\nDepartment: ",student["department"])
                                  print("\n Current CGPA: ",student["cgpa"])
                                  print("\n------------------") 
                            
          except FileNotFoundError:
            print("file Not found")
    def deleteStudent(self):
      try: 
          id=int(input("\nEnter the Student id which you want to delete"))
          pin=int(input("Enter the pin (Because it is security): "))
          if pin==1122:
                with open("Student.json","r") as f:
                      students=json.load(f)
                      for student in students:
                            if id==student["student_id"]:
                              students.remove(student)
                              break
                with open("Student.json","w") as f:
                      json.dump(students,f,indent=4)
      except FileNotFoundError:
            print("Sorry! File not found")              
                
    def  update_Student(self):
        
        try:
                id=int(input("\nEnter the Student for update Student Details:")) 
                selected=None
                
                
             
                   
                with open("Student.json", "r") as f:
                 Students = json.load(f)

               #  print(type(Students))

                for i, student in enumerate(Students):
                    # print(i, student)

                    if "student_id" not in student:
                        print("Problem record:", student)
                        continue

                    if student["student_id"] == id:
                        selected = student
                        print("Found", selected)
                if selected is None:
                     print("\nSorry Student id is not found")
                     return
                        
                while True:
                            print("1. Student Name")
                            print("2. Father Name")
                            print("3. Age")
                            print("4. Semester")
                            print("5. CGPA")
                            print("6. Phone Number")
                            print("7. Email")
                           
                            a=int(input("Enter Your Choice"))

                            if a==1: 
                                  while True:
                                  
                                     name=input("\nEnter Your Full Name(Must be in Latters)")
                                    
                                     if name.replace(" ","").isalpha():
                                        print("\nYour Name is Valid!")
                                        selected["student_name"]=name
                                        print("Student Name update Successfully")
                                        with open("Student.json","w") as f:
                                         json.dump(Students,f,indent=4)
                                        break
                                         
                                    
                                     else:
                                      print("\nRe-Enter Your Name!")
                            elif a==2:
                                  while True:
                                        fathername=input("\nEnter Your Father Name(Must be in Latters)")
                                                           
                                        if fathername.replace(" ","").isalpha():
                                                               print("\nFather Name is Valid!")
                                                               selected["father_name"]=fathername
                                                               with open("Student.json","w") as f:
                                                                 json.dump(Students,f,indent=4)
                                                                 print("\n FatherName Updated")

                                                               break
                                        else:
                                                               print("\nRe-Enter Your Name!")
                            elif a==3:
                                  while True:
                                              
                                                    age=int(input("\nEnter Your Age"))
                                                    if age in range(15,61):
                                                         print("\nYour are Eligible")
                                                         selected["age"]=age
                                                         
                                                         with open("Student.json","w") as f:
                                                            json.dump(Students,f,indent=4)
                                                            print("\n Age Updated!")
                                                         

                                                         break
                                                    else:
                                                         print('\nYou are not eligible to apply')
                            elif a==4:
                                  while True:
                                            
                                                      n=float(input("\nEnter Your Cgpa (must in 0.0-4.0)"))
                                                      if 0.0 <= n <= 4.0:
                                                           selected["cgpa"]=n
                                                           with open("Student.json","w") as f:
                                                            json.dump(Students,f,indent=4)
                                                            print("\n Cgpa UPdated!")
                                                                                                                    
                                                           break
                                                      else:
                                                           print("\nplease Enter your Cgpa (must in 0.0-4.0) ")
                            elif a==5:
                                  while True:
                                                 sem=int(input("\nPlease Enter Your Semester"))
                                                 semester=(1,2,3,4,5,6,7,8)
                                  
                                                         
                                                 if sem in semester:
                                                        selected["semester"]=sem
                                                        with open("Student.json","w") as f:
                                                         json.dump(Students,f,indent=4)
                                                         print("\nSemester Updated")
                                                        break
                                                 else:
                                                       print("\nPlease Re_enter Your Semester!")
                            elif a==6:
                                   while True:
                                        phone=input("Enter Your Phone No")
                                                
                                        phone=(input("\nEnter Your phone no (must in 11 Digit)"))
                                        if phone.isdigit() and len(phone)==11:
                                             selected["phone_no"]=phone
                                             with open("Student.json","w") as f:
                                              json.dump(Students,f,indent=4)
                                              print("\nPhone No updated")

                                             break
                                        else:
                                              print("\nplease Enter your phone (must in 11 digit) ")
                            elif a==7:
                                   while True:
                                               email=input("Enter your Email(Your Email must in @format):")
                                               if '@' in email and '.' in email:
                                                        print("Valid email! ")
                                                        selected["email"]=email
                                                        with open("Student.json","w") as f:
                                                         json.dump(Students,f,indent=4)
                                                         print("\n Email Updated!")
                                                        break

                                               else:

                                                        print("Your Email is invalid!")
                    
        except FileNotFoundError:
           print("FIle not FOund")   
    def export_to_csv(self):
      try:
        with open("Student.json", "r") as f:
            students = json.load(f)

        if not students:
            print("\nNo student records found.")
            return

        with open("Students.csv", "w", newline="") as f:

            fieldnames = students[0].keys()

            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(students)

        print("\nStudent data successfully exported to Students.csv")

      except FileNotFoundError:
        print("\nStudent.json not found.")                            

    def Higestcgpa(self):
      highest_cgpa = 0.0
      Higestcgpa_student = None
      
      try:
          with open("Student.json", "r") as f:
              students = json.load(f)
              for student in students:
                    if student["cgpa"] > highest_cgpa:
                        highest_cgpa = student["cgpa"]
                        Higestcgpa_student = student
          print("\nStudent with the highest CGPA:")
          print("\nID:", Higestcgpa_student["student_id"])
          print("\nName:", Higestcgpa_student["student_name"])
          print("\nCGPA:", Higestcgpa_student["cgpa"])
      except FileNotFoundError:
       print("\nStudent.json not found.")  
    def lowestcgpa(self):
      lowest_cgpa = 0.0
      lowest_cgpa = float("inf")
      
      try:
          with open("Student.json", "r") as f:
              students = json.load(f)
              for student in students:
                    if student["cgpa"] < lowest_cgpa:
                        lowest_cgpa = student["cgpa"]
                        lowest_cgpa_student = student
          print("\nStudent with the lowest CGPA:")
          print("\nID:", lowest_cgpa_student["student_id"])
          print("\nName:", lowest_cgpa_student["student_name"])
          print("\nCGPA:", lowest_cgpa_student["cgpa"])
      except FileNotFoundError:
       print("\nStudent.json not found.")
    def semestersearch(self):
          try:
                s=int(input("Enter the semester which you want to search"))
                if s in range(1,9):
                      with open("Student.json","r") as f:
                            students=json.load(f)
                            for student in students:
                                  if student["semester"]==s:
                                        print("\n------------------")  
                                        print("\nFound: ",student["student_id"])
                                        print("\nStudent Name : ",student["student_name"])  
                                        print("\nDepartment: ",student["department"])
                                        print("\n Current CGPA: ",student["cgpa"])
                                        print("\n------------------")
                else:
                    print("\nPlease Enter the semester in range of 1-8")
          except FileNotFoundError:   
                print("\nFile Not Found")  

    def departmentsearch(self):
          try:
                d=input("Enter the department which you want to search")
                dep1=("Software Engineering",'Computer Science',"Artifical Inteligence","Computer Engineering") 
                if d in dep1:
                      with open("Student.json","r") as f:
                            students=json.load(f)
                            for student in students:
                                  if student["Department"]==d:
                                        print("\n------------------")  
                                        print("\nFound: ",student["student_id"])
                                        print("\nStudent Name : ",student["student_name"])  
                                        print("\nDepartment: ",student["department"])
                                        print("\n Current CGPA: ",student["cgpa"])
                                        print("\n------------------")
                else:
                    print("\nPlease Enter the department in following options"
                    "(Software Engineering,Computer Science,Artifical Inteligence,Computer Engineering)")
          except FileNotFoundError:   
                print("\nFile Not Found")
     
                               

StudentManager1=StudentManager()
StudentManager1.export_to_csv()                             
                              
                              
                              
                                        



                                                   
                                  
                                  
                       
                            
                                        
                                     
                