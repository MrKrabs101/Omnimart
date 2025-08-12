from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection, execute_query

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# 🏠 Homepage
@app.route("/")
def homepage():
    products = execute_query("SELECT asin, title, brand, final_price, currency, rating, image_url FROM products LIMIT 20", fetch=True, dictionary=True)
    return render_template("index.html", products=products)

# 🔍 Product Detail
@app.route("/product/<asin>")
def product_detail(asin):
    product = execute_query("SELECT * FROM products WHERE asin = ?", (asin,), fetch=True, dictionary=True)
    if not product:
        return "Product not found", 404
    return render_template("product_detail.html", product=product[0])

# ➕ Add to Cart (AJAX)
@app.route("/add-to-cart/<asin>", methods=["POST"])
def add_to_cart(asin):
    if request.is_json:
        data = request.get_json()
        qty = int(data.get("qty", 1))
    else:
        return jsonify({"error": "Invalid content type"}), 415

    product = execute_query("SELECT title, final_price, image_url FROM products WHERE asin = ?", (asin,), fetch=True, dictionary=True)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    item = product[0]
    cart = session.get("cart", {})

    if asin in cart:
        cart[asin]["qty"] += qty
    else:
        cart[asin] = {
            "title": item["title"],
            "price": float(item["final_price"]),  # ✅ Make sure this is a float
            "qty": qty,
            "img": item["image_url"]
        }

    session["cart"] = cart
    return jsonify({"message": "Added to cart"}), 200


# 🛒 Cart Page
@app.route("/cart")
def cart():
    cart = session.get("cart", {})
    return render_template("cart.html", cart=cart)

# 🔄 Update Cart
@app.route("/update-cart/<asin>/<action>")
def update_cart(asin, action):
    cart = session.get("cart", {})
    if asin in cart:
        if action == "increase":
            cart[asin]["qty"] += 1
        elif action == "decrease":
            cart[asin]["qty"] -= 1
            if cart[asin]["qty"] <= 0:
                del cart[asin]
        elif action == "remove":
            del cart[asin]
    session["cart"] = cart
    return redirect("/cart")

# 👤 Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        execute_query("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        return redirect("/login")
    return render_template("signup.html")

# 🔐 Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = execute_query("SELECT * FROM users WHERE email = ?", (email,), fetch=True, dictionary=True)
        if user and check_password_hash(user[0]["password"], password):
            session["user_id"] = user[0]["id"]
            session["user_name"] = user[0]["name"]
            return redirect("/")
        return "Invalid email or password"
    return render_template("login.html")

# 🚪 Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
