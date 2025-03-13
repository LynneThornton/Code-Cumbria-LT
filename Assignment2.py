import sqlite3
import matplotlib.pyplot as plt
import pandas as pd

# Connect to (or create) a database file
conn = sqlite3.connect("Company.db")

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

 # Create departments table
cursor.execute("""
CREATE TABLE IF NOT EXISTS departments (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 name TEXT UNIQUE NOT NULL
)
""")

cursor.execute("""
DROP TABLE employees;""")

# Create employees table with a foreign key to departments
cursor.execute("""
CREATE TABLE employees (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  age INTEGER,
  department_id INTEGER,
  salary REAL,
  FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE
 )
 """)

conn.commit()
print("Database schema updated with relational tables!") 

# Insert departments
departments = [("HR",), ("IT",), ("Finance",), ("Marketing",)]
cursor.executemany("INSERT OR IGNORE INTO departments (name) VALUES (?)", departments)
conn.commit()
print("Departments inserted successfully!")

# Fetch department IDs
cursor.execute("SELECT id, name FROM departments")
departments_dict = {name: dept_id for dept_id, name in cursor.fetchall()} # {'HR': 1, 'IT': 2, ...}

# Fetch department IDs
cursor.execute("SELECT id, name FROM departments")
departments_dict = {name: dept_id for dept_id, name in cursor.fetchall()} # {'HR': 1, 'IT': 2, ...}

# Insert employees with department IDs
employees = [
  ("Alice", 30, departments_dict["HR"], 50000),
  ("Bob", 25, departments_dict["IT"], 60000),
  ("Charlie", 35, departments_dict["Finance"], 70000),
  ("David", 28, departments_dict["Marketing"], 55000),
]
cursor.executemany("INSERT INTO employees (name, age, department_id, salary) VALUES (?, ?, ?, ?)", employees)
conn.commit()
print("Employees inserted successfully!")

# Add Employees
def add_employee():
  name = input("Enter name: ")
  age = int(input("Enter age: "))
  department = input("Enter department: ")
  salary = float(input("Enter salary: "))
  cursor.execute("INSERT INTO employees (name, age, department, salary) VALUES(?, ?, ?, ?)",(name, age, department, salary))
  conn.commit()
  print(f"\nEmployee {name} added successfully!\n")

# Add Department
def add_department():
  name = input("Enter department: ")
  cursor.execute("INSERT INTO employees (name, age, department, salary) VALUES(?, ?, ?, ?)",(name, age, department, salary))
  conn.commit()
  print(f"\nEmployee {name} added successfully!\n")

# View Employees
def view_employees():
  cursor.execute("SELECT * FROM employees")
  employees = cursor.fetchall()
  if not employees:
    print("\nNo employees found.\n")
  else:
    print("\nEmployee List:")
  for emp in employees:
      print(emp)

# Update Employee
def update_employee():
  emp_id = int(input("Enter Employee ID to update: "))
  cursor.execute("SELECT * FROM employees WHERE id = ?", (emp_id,))
  employee = cursor.fetchone()
  if not employee:
    print("\nEmployee not found!\n") 
    return
  print("\nUpdating Employee:", employee)
  name = input("Enter new name (or press Enter to keep the same): ") or employee[1]
  age = input("Enter new age (or press Enter to keep the same): ")
  department = input("Enter new department (or press Enter to keep the same): ") or employee[3]
  salary = input("Enter new salary (or press Enter to keep the same): ")
 # Convert inputs if they are not empty
  age = int(age) if age else employee[2]
  salary = float(salary) if salary else employee[4]
  cursor.execute("UPDATE employees SET name = ?, age = ?, department = ?, salary = ? WHERE id = ?",(name, age, department, salary, emp_id))
  conn.commit()
  print(f"\nEmployee ID {emp_id} updated successfully!\n")

# Delete Employee
def delete_employee():
   emp_id = int(input("Enter Employee ID to delete: "))
   cursor.execute("SELECT * FROM employees WHERE id = ?", (emp_id,))
   employee = cursor.fetchone()
   if not employee:
    print("\nEmployee not found!\n")
    return
   confirm = input(f"Are you sure you want to delete {employee[1]}? (yes/no): ").lower()
   if confirm == "yes":
    cursor.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
    conn.commit()
    print(f"\nEmployee ID {emp_id} deleted successfully!\n")
   else:
    print("\nDelete action canceled.\n")

# View employees with department names
def employee_department():
  cursor.execute("""
  SELECT employees.id, employees.name, departments.name
  FROM employees
  JOIN departments ON employees.department_id = departments.id
  """)
  employees_with_departments = cursor.fetchall()
  print("\nEmployee Details with Department Names:")
  for emp in employees_with_departments:
    print(emp) 

# Query how many employees are in each department
def employee_count_by_dept():
    cursor.execute("""
    SELECT COUNT(employees.department_id) AS empcount, departments.name AS dept
    FROM employees
    JOIN departments ON employees.department_id = departments.id
    GROUP BY departments.name
    """)
    employees_departments_count = cursor.fetchall()

    print("\nEmployee Count with Department Names:")
    for emp in employees_departments_count:
        print(emp) 
    df = pd.DataFrame.from_records(employees_departments_count)
    # Create bar chart of Employee Count by Department
    plt.figure(figsize=(8, 5))
    df.plot(kind="bar", color="skyblue")
    plt.title("Number of Employees per Department")
    plt.xlabel("Department")
    plt.ylabel("Number of Employees")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

# Create a user menu
def menu():
    while True:
            print("\nEmployee Management System")
            print("1. Add Employee")
            print("2. View Employees")
            print("3. Update Employee")
            print("4. Delete Employee")
            print("5. Add Department")
            print("6. Show Employee Count by Department")
            print("7. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                add_employee()
            elif choice == "2":
                view_employees()
            elif choice == "3":
                update_employee()
            elif choice == "4":
                delete_employee()
            elif choice == "5":
                add_department()
            elif choice == "6":
                employee_count_by_dept()
            elif choice == "7":
                print("\nExiting... Goodbye!")
                conn.close() 
                break
            else:
                print("\nInvalid choice! Please enter a number between 1 and 7.\n")
# Run the menu
menu()