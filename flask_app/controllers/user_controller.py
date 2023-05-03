from flask import render_template, redirect, request, session

from flask_bcrypt import Bcrypt

from flask_app import app
from flask_app.models.user import User

bcrypt = Bcrypt(app)



#INDEX HOME PAGE
@app.route("/")
def index():
    if "uuid" in session:
        return redirect("/dashboard")

    return render_template ("index.html")


#REGISTER - POST
@app.route("/register", methods = ["POST"])
def register():
    if not User.register_validator(request.form):
        return redirect("/")

    passw_hash = bcrypt.generate_password_hash(request.form ["password"])
    data = {
        **request.form,
        "password": passw_hash
    }

    user_id = User.create(data)

    session["uuid"] = user_id

    return redirect("/dashboard")


#LOGIN - POST
@app.route("/login", methods = ["POST"])
def login():
    if not User.login_validator(request.form):
        return redirect("/")

    user = User.get_by_email({ "email": request.form["email"] })

    session["uuid"] = user.id

    return redirect("/dashboard")


#LOGOUT
@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")




