# 🎓 Student Management System

A console-based **Student Management System built with Python** using Object-Oriented Programming (OOP), JSON file handling, authentication, data validation, CRUD operations, and CSV export.

---

## 📌 Project Overview

The **Student Management System** is a Python-based application designed to manage student records efficiently through a simple command-line interface.

The system provides separate **Admin** and **User** functionality. Admins can manage student records, while users can log in and access student information.

This project was developed to gain practical experience with **Python, OOP, file handling, JSON, CSV, exception handling, authentication, and modular programming**.

---

## ✨ Features

### 🔐 Authentication

* User Sign Up
* User Login
* Admin Login
* Forgot Password functionality
* Password validation
* Email validation

### 👨‍🎓 Student Management

Admin can:

* Add Student
* View Student
* Update Student
* Delete Student
* Search Student by ID

### 📊 Student Analysis

* Department-wise Student Search
* Semester-wise Student Search
* Highest CGPA Student
* Lowest CGPA Student

### 📁 Data Management

* Store user information in JSON
* Store student records in JSON
* Export student records to CSV
* Automatic Student ID generation
* Read and write JSON data

### 🛡️ Security

The system includes basic security mechanisms:

* Admin authentication
* User authentication
* Password validation
* Forgot Password functionality
* PIN verification before deleting student records

---

## 🔑 Student Delete Security PIN

Before deleting a student record, the system requires a security PIN.

### Current Demo PIN

```text
1122
```

The PIN is currently implemented in the Python code:

```python
if pin == 1122:
```

If you want to change the PIN, you can directly modify this value in the relevant Python file.

> **Note:** In a future version, the PIN can be moved to a secure configuration file or database instead of keeping it directly in the source code.

---

## ✅ Input Validation

The system validates:

* Student name
* Father's name
* Age
* Gender
* Department
* CGPA
* Email
* Phone number
* Semester
* Password

---

## 🛠️ Technologies Used

* **Python**
* **Object-Oriented Programming (OOP)**
* **JSON**
* **CSV**
* **File Handling**
* **Exception Handling**
* **Modular Programming**

The current version uses Python's built-in libraries, so no external packages are required.

---

## 🧱 OOP Concepts Used

This project applies several important Python OOP concepts:

* Classes and Objects
* Constructors
* Instance Variables
* Class Variables
* Instance Methods
* Encapsulation
* Modular Programming

---

## 📂 Project Structure

```text
Student-Management-System/
│
├── main.py
├── Student.py
├── StudentManager.py
├── auth.py
├── forgot.py
│
├── README.md
├── .gitignore
│
└── Data Files
    ├── data.json
    ├── Student.json
    └── Students.csv
```

> **Note:** `data.json`, `Student.json`, and `Students.csv` may contain user/student information and are excluded from the GitHub repository using `.gitignore`.

---

## 🔄 Application Flow

```text
Start Application
       │
       ▼
   Main Menu
       │
       ├── Admin Login
       │      │
       │      ├── Add Student
       │      ├── View Student
       │      ├── Update Student
       │      ├── Search Student
       │      ├── Department Search
       │      ├── Semester Search
       │      ├── Highest CGPA
       │      ├── Lowest CGPA
       │      └── Export CSV
       │
       ├── User Login
       │      │
       │      ├── View Student
       │      ├── Update Student
       │      └── Search Student
       │
       ├── Sign Up
       │
       ├── Forgot Password
       │
       └── Exit
```

---

## ▶️ How to Run

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
```

### 2. Open the Project Directory

```bash
cd Student-Management-System
```

### 3. Run the Application

```bash
python main.py
```

---

## 🔑 Demo Admin Login

For demonstration purposes:

```text
Username: admin
Password: admin
```

> These credentials are currently hardcoded for this learning project. A production system should use a secure authentication mechanism.

---

## 💾 Data Storage

The current version uses **JSON files** for data persistence.

### User Data

```text
data.json
```

This file stores user authentication information.

### Student Data

```text
Student.json
```

This file stores student records.

### CSV Export

Student records can be exported to:

```text
Students.csv
```

This allows the data to be opened and analyzed using spreadsheet or data-analysis tools.

---

## 🚀 Future Improvements

Planned improvements for future versions include:

* 🖥️ GUI frontend
* 🗄️ MySQL database integration
* 🔐 Password hashing
* 🔑 Improved authentication
* 💾 Backup and Restore functionality
* 🌐 Web-based version
* 📊 Advanced student statistics
* 🔎 Improved search functionality
* 🧹 Reusable validation methods
* 🏗️ Improved project architecture
* 📈 Data analysis using NumPy and Pandas

---

## 🎯 Learning Objectives

This project helped strengthen practical knowledge of:

* Python Programming
* Object-Oriented Programming
* Classes and Objects
* Encapsulation
* File Handling
* JSON Handling
* CSV Handling
* Exception Handling
* CRUD Operations
* Authentication
* Input Validation
* Modular Programming
* Basic Data Management

---

## 👨‍💻 Author

### Ali Adrees

**Software Engineering Student**
COMSATS University Islamabad, Sahiwal Campus

### Interests

* Python
* Artificial Intelligence
* Machine Learning
* Software Engineering
* Data Science

---

## 📌 Project Status

**Current Status: Completed — Console-Based Version**

The current version is a Python console application.

Future versions may include a **GUI frontend, MySQL database, and additional security features**.

---

## 📄 License

This project was created for **educational and learning purposes**.
