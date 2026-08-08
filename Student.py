import json
class Student:
   
    def __init__(self,std_name,fath_name,age,gen,dep,sem,cg,phno,email):
        self.student_name=std_name
        self.father_name=fath_name
        self.age=age
        self.gender=gen
        self.semester=sem
        self.cgpa=cg
        self.phone_no=phno
        self.email_address=email
        self.department=dep
       
        self.student_id = self.get_next_id()

    def get_next_id(self):
        try:
            with open("data/Student.json", "r") as f:
                students = json.load(f)

            if not students:
                return 1

            return max(student["student_id"] for student in students) + 1

        except (FileNotFoundError, json.JSONDecodeError):
            return 1

    def to_dic(self):
        s={
            "student_id":self.student_id,
          "student_name":self.student_name,
          "father_name":self.father_name,
          "age": self.age,
          "Department":self.department,
          "gender":self.gender,
          "semester":self.semester,
          "cgpa":self.cgpa,
          "phone_no":self.phone_no,
          "email_address":self.email_address




        }
        return s
    def save(self,s):
          try:
               with open("Student.json","r") as f:
                    users=json.load(f)
                    users.append(s)
               with open("Student.json","w") as f:
                    json.dump(users,f,indent=4)
          except FileNotFoundError:
               print("\nSorry, FIle is not found")



