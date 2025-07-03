from my_app import app, session, render_template, redirect, request, flash
from my_app.models.users import User
from datetime import datetime

@app.route("/main_page")
def main_page():
    if "user_id" not in session:
        flash ("Please login before using this page!")
        return redirect(request.referrer)
    my_user= User.get_user_by_id["id":session["user_id"]]
    return render_template("main.html", current_user = my_user)