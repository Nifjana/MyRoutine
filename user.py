from my_app import app, redirect, render_template, request, flash
from flask import session
from my_app.models.users import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def first_page():
    return render_template("login.html")

@app.route("/reg")
def singup():
    return render_template("register.html")

@app.route("/register", methods = ["POST"])
def register():
    if User.get_user_by_email(request.form) :
        flash("This user already exist! Try another one.")
        return redirect(request.referrer)
    if not User.validate_user(request.form):
        return redirect(request.referrer)
    user = {
        "name" : request.form["name"],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form["password"]),
        "confpass": request.form["confpass"]
    }
    User.create_user(user)
    return redirect("/main_page")


@app.route("/login", methods=["POST"])
def login():
    user = User.get_user_by_email({"email":request.form['email']})
    if not user:
        flash("This email does not exist! Try again.")
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(user["password"], request.form["password"]):
        flash("Password or email is not correct! Please try again.")
        return redirect(request.referrer)
    session["user_id"] = user["id"]
    print("SESSION NOW:", session)

    return redirect("/main_page")
    

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
