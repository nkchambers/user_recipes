
from flask import flash
from flask_bcrypt import Bcrypt

from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import recipe


bcrypt = Bcrypt(app)

class User:
    schema = "user_recipes"
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.recipes = []



    #READ MANY
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.schema).query_db(query) 

        if len(results) < 1:
            return False

        return User(results[0])


    #READ ONE
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.schema).query_db(query, data) 

        if len(results) < 1:
            return False

        return User(results[0])


    #READ ONE
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.schema).query_db(query, data) 

        if len(results) < 1:
            return False

        return User(results[0])


    #CREATE
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        
        return connectToMySQL(cls.schema).query_db(query, data)



    
    #VALIDATE - REGISTRATION FORM
    @staticmethod
    def register_validator(post_data):
        is_valid = True

        if len(post_data["first_name"]) < 2:
            flash("First Name must be at least 2 characters.")
            is_valid = False

        if len(post_data["last_name"]) < 2:
            flash("Last Name must be at least 2 characters.")
            is_valid = False

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data["email"]): 
            flash("Invalid Email Address!")
            is_valid = False
        else:
            user = User.get_by_email({"email": post_data["email"]})
            if user:
                flash("Email is already in use!")
                is_valid = False

        if len(post_data["password"]) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False

        if post_data["password"] != post_data["confirm_password"]:
            flash("Password and confirm password must match.")
            is_valid = False


        return is_valid


    #VALIDATE - LOGIN FORM
    @staticmethod
    def login_validator(post_data):
        user = User.get_by_email({"email": post_data["email"]})

        if not user:
            flash("Invalid Email/Password")
            return False


        if not bcrypt.check_password_hash(user.password, post_data["password"]):
            flash("Invalid Email/Password")
            return False

        
        return True

