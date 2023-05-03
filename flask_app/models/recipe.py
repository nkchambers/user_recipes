from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user


class Recipe:
    schema = "user_recipes"
    def __init__(self, data):
        self.id = data["id"]
        self.user = user.User.get_by_id({ "id": data["user_id"] })
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_made_on = data["date_made_on"]
        self.under_half_hour = data["under_half_hour"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    #CREATE
    @classmethod
    def create(cls, data):
        pass

    
    #READ MANY
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.schema).query_db(query) 

        recipes = []
        for row in results:
            recipes.append(cls(row))

        return recipes


    #READ ONE
    @classmethod
    def get_one(cls, data):
        pass


    #UPDATE
    @classmethod
    def update(cls, data):
        pass


    #DELETE
    def delete(cls, data):
        pass




    #VALIDATIONS
    @staticmethod
    def validate(post_data):
        pass