from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection, execute_query

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

@app.route("/")
def homepage():
    products = execute_query("SELECT * FROM products", fetch=True, dictionary=True)
    return render_template("index.html", products=products)

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        # Insert user into database
        execute_query(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_password)
        )

        return redirect("/login")

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Fetch user from database
        user = execute_query(
            "SELECT * FROM users WHERE email = %s",
            (email,),
            fetch=True,
            dictionary=True
        )

        if user and check_password_hash(user[0]["password"], password):
            session["user_id"] = user[0]["id"]
            session["user_name"] = user[0]["name"]
            return redirect("/")
        else:
            return "Invalid email or password"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
