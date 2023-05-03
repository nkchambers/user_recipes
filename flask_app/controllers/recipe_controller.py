from flask import render_template, redirect, request, session

from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe









#SHOW DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "uuid" not in session:
        return redirect("/")


    return render_template(
            "dashboard.html", 
            logged_in_user = User.get_by_id({"id": session["uuid"]}),
            all_recipes = Recipe.get_all()
    )
