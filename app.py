from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

DATABASE = "database.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            age INTEGER,
            department TEXT,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    email = request.form["email"]
    age = request.form["age"]
    department = request.form["department"]
    message = request.form["message"]

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name,email,age,department,message) VALUES (?,?,?,?,?)",
        (name, email, age, department, message)
    )
    conn.commit()
    conn.close()

    return render_template("thankyou.html", name=name)

# Initialize database when app starts
init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
