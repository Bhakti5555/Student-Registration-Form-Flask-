from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# connect to database
mydb = mysql.connector.connect(
    host= "localhost",
    user="root",
    password= "root",
    database="flask_students"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/add")
def add_student():
    return render_template("add_student.html")

@app.route("/view")
def view_students():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()   # list of tuples

    return render_template("view_students.html", students=data)

@app.route("/search", methods=["GET", "POST"])
def search_student():
    student = None

    if request.method == "POST":
        roll = request.form["roll"]

        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM students WHERE roll = %s", (roll,))
        student = cursor.fetchone()

    return render_template("search.html", student=student)

@app.route("/delete", methods=["GET", "POST"])
def delete_student():
    message = None

    if request.method == "POST":
        roll = request.form["roll"]

        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM students WHERE roll = %s", (roll,))
        student = cursor.fetchone()

        if student:
            cursor.execute("DELETE FROM students WHERE roll = %s", (roll,))
            mydb.commit()
            message = f"Student with Roll No {roll} deleted successfully!"
        else:
            message = "No student found with that roll number."

    return render_template("delete.html", message=message)


@app.route("/student", methods=["GET", "POST"])
def students():
    if request.method == "POST":
        name = request.form["name"]
        roll = request.form["roll"]
        branch = request.form["branch"]
        year = request.form["year"]
        phone = request.form["phone"]

        cursor = mydb.cursor()
        sql = "INSERT INTO students (name, roll, branch, year, phone) VALUES (%s, %s, %s, %s, %s)"
        values = (name, roll, branch , year, phone)
        cursor.execute(sql, values)
        mydb.commit()

        return "Students added successfully!"
    
    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)