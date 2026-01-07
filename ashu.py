import mysql.connector
import datetime as dt
import sys

# -------------------------------
# DATABASE CONNECTION
# -------------------------------
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",  
        database="employee_db",
        charset="utf8",
        use_unicode=True
    )
    cur = conn.cursor()
except mysql.connector.Error as err:
    print("❌ ERROR: Could not connect to MySQL")
    print("DETAILS:", err)
    sys.exit()

# -------------------------------
# DEVELOPER INFORMATION 
# -------------------------------
terminal_width = 80
print("=" * terminal_width)
print("🖥️  EMPLOYEE MANAGEMENT SYSTEM  🖥️".center(terminal_width))
print("=" * terminal_width)
print("\n")
print("🔹 DEVELOPER DETAILS 🔹".center(terminal_width))
print("\n")
print("CREATED BY           : ASHUTOSH PANDEY".center(terminal_width))
print("ROLE                 : SOFTWARE DEVELOPER / STUDENT".center(terminal_width))
print("MENTOR / GUIDED BY   : MANOJ KHARE (PGT CS)".center(terminal_width))
print("INSTITUTION          : JAWAHAR NAVODAYA VIDYALAYA, PRATAPGARH (UP)".center(terminal_width))
print("PROJECT              : EMPLOYEE MANAGEMENT SYSTEM".center(terminal_width))
print("VERSION              : 1.0.0".center(terminal_width))
print("DATE OF CREATION     : 06/11/2025".center(terminal_width))
print("\n")
print("📌 NOTE: THIS SOFTWARE IS DEVELOPED FOR EDUCATIONAL PURPOSES".center(terminal_width))
print("📌 ENSURE DATA IS ENTERED CAREFULLY TO AVOID ERRORS".center(terminal_width))
print("\n")
print("=" * terminal_width)
print("\n"*1)

# -------------------------------
# AUTO CREATE TABLES
# -------------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS log_id (
    user_id VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS office (
    em_id INT PRIMARY KEY,
    em_name VARCHAR(50),
    em_dept VARCHAR(50),
    em_salary FLOAT,
    em_age INT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS em_performance (
    em_id INT,
    em_name VARCHAR(50),
    em_dept VARCHAR(50),
    performance VARCHAR(100),
    experience INT
)
""")
conn.commit()

# -------------------------------
# WELCOME SCREEN
# -------------------------------
print("=" * 50)
print("      WELCOME TO EMPLOYEE MANAGEMENT SYSTEM")
print("=" * 50)
print("Current Date & Time:", dt.datetime.now())

# -------------------------------
# LOGIN / REGISTER LOOP
# -------------------------------
while True:
    print("\n1. REGISTER")
    print("2. LOGIN")
    choice = input("Enter your choice: ")

    if choice == '1':
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        try:
            cur.execute(
                "INSERT INTO log_id VALUES (%s, %s)",
                (username, password)
            )
            conn.commit()
            print("\n✅ User registered successfully!")
        except mysql.connector.Error:
            print("❌ Username already exists! Try logging in.")
        cont = input("Do you want to login now? (y/n): ").lower()
        if cont == 'y':
            continue
        else:
            print("You can restart the program anytime to login.")
            break

    elif choice == '2':
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        cur.execute(
            "SELECT * FROM log_id WHERE user_id=%s AND password=%s",
            (username, password)
        )
        result = cur.fetchone()
        if result:
            print("\n✅ Login successful!")
            break
        else:
            print("❌ Invalid username or password! Try again.")
    else:
        print("❌ Invalid choice! Enter 1 or 2.")

# -------------------------------
# FUNCTION DEFINITIONS
# -------------------------------
def register_employee():
    eid = int(input("Employee ID: "))
    name = input("Name: ")
    dept = input("Department: ")
    salary = float(input("Salary: "))
    age = int(input("Age: "))
    cur.execute(
        "INSERT INTO office VALUES (%s, %s, %s, %s, %s)",
        (eid, name, dept, salary, age)
    )
    conn.commit()
    print("✅ Employee registered successfully!")

def show_details():
    cur.execute("SELECT * FROM office")
    rows = cur.fetchall()
    if not rows:
        print("❌ No employee records found.")
        return
    print("\n--- EMPLOYEE DETAILS ---")
    for row in rows:
        print(row)

def update_salary():
    name = input("Enter Employee Name: ")
    cur.execute("SELECT em_salary FROM office WHERE em_name=%s", (name,))
    current = cur.fetchone()
    if not current:
        print("❌ Employee not found!")
        return
    print("Current Salary of", name, "is:", current[0])
    print("Choose an option:")
    print("1. Give fixed increment")
    print("2. Set new salary")
    choice = input("Enter 1 or 2: ")
    if choice == '1':
        inc = float(input("Enter increment amount: "))
        cur.execute(
            "UPDATE office SET em_salary = em_salary + %s WHERE em_name=%s",
            (inc, name)
        )
    elif choice == '2':
        new_sal = float(input("Enter new salary: "))
        cur.execute(
            "UPDATE office SET em_salary = %s WHERE em_name=%s",
            (new_sal, name)
        )
    else:
        print("❌ Invalid choice!")
        return
    conn.commit()
    print("✅ Salary updated successfully!")

def employee_list():
    cur.execute("SELECT em_name FROM office ORDER BY em_name")
    rows = cur.fetchall()
    if not rows:
        print("❌ No employees found.")
        return
    print("\n--- EMPLOYEES LIST ---")
    for row in rows:
        print(row[0])

def employee_count():
    cur.execute("SELECT COUNT(*) FROM office")
    count = cur.fetchone()
    print("Total Employees:", count[0])

def add_performance():
    eid = int(input("Employee ID: "))
    name = input("Name: ")
    dept = input("Department: ")
    perf = input("Performance Remarks: ")
    exp = int(input("Experience (years): "))
    cur.execute(
        "INSERT INTO em_performance VALUES (%s, %s, %s, %s, %s)",
        (eid, name, dept, perf, exp)
    )
    conn.commit()
    print("✅ Performance record added!")

def view_salary():
    name = input("Employee Name: ")
    cur.execute("SELECT em_salary FROM office WHERE em_name=%s", (name,))
    sal = cur.fetchone()
    if sal:
        print("Salary:", sal[0])
    else:
        print("❌ Employee not found!")

# -------------------------------
# MAIN MENU LOOP
# -------------------------------
while True:
    print("\n========= EMPLOYEE MANAGEMENT MENU =========")
    print("1. Employee Registration")
    print("2. Display Employee Details")
    print("3. Update Employee Salary")
    print("4. Display Employees List")
    print("5. Count Total Employees")
    print("6. Add Performance Record")
    print("7. View Employee Salary")
    print("8. Exit")
    print("============================================")

    ch = input("Enter your choice: ")

    if ch == '1':
        register_employee()
    elif ch == '2':
        show_details()
    elif ch == '3':
        update_salary()
    elif ch == '4':
        employee_list()
    elif ch == '5':
        employee_count()
    elif ch == '6':
        add_performance()
    elif ch == '7':
        view_salary()
    elif ch == '8':
        print("Thank you for using Employee Management System!")
        break
    else:
        print("❌ Invalid choice! Try again.")

conn.close()
