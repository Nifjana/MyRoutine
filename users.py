from my_app.config.mysqlconn import connect_to_mysql
import re
from flask import flash

class User:
    mydb = "instagram_schema"

    def __init__(self,data):
        self.id = data["id"]
        self.name = data["name"]
        self.email = data["email"]
        self.password= data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
  
    @classmethod
    def create_user(cls,data):
        query = 'INSERT INTO users(name, email, password) VALUES(%(name)s,%(email)s,%(password)s)'
        result = connect_to_mysql("mydb").query_db(query,data)
        return result
    
    @classmethod
    def get_users(cls):
        query = "SELECT * FROM users"
        result = connect_to_mysql("mydb").query_db(query)
        if not result:
            return[]
        my_users = []
        for i in result:
            my_users.append(cls(i))
        return my_users
    
    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * From users WHERE email = s(email)%"
        result = connect_to_mysql("mydb").query_db(query,data)
        if result and len(result) > 0:
            return result[0]
        return False
    
    @classmethod
    def get_user_by_id(cls,data):
        query = "SELECT * WHERE id = s(id)%"
        result = connect_to_mysql("mydb").query_db(query,data)
        if result:
            return cls(result[0])
    
    
    @classmethod
    def update_users(cls,data):
        query = "UPDATE users SET name = %(name)s WHERE id = %(id)s"
        result= connect_to_mysql("mydb").query_db(query,data)
        if result is None:
            return []
        return result
    
    @classmethod
    def delete_user(cls,data):
        query = "DELETE FROM users WHERE id = s(id)% "
        return connect_to_mysql("mydb").query_db(query,data)
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(user["name"]) < 2 or len(user["name"]) > 45:
            flash("First name must be between 2 and 45 characters!!!", "Name")
            is_valid = False
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid email or password!!!", "emailSignUp")
            is_valid = False
        else:
            if User.get_user_by_email({"email": user["email"]}):
                flash("Email already in use!", "emailSignUp")
                is_valid = False
        if len(user['password']) < 8:
            flash("Password must at least 8 characters!!!", "password")
            is_valid = False
        if user["confpass"] != user["password"]:
            flash("The passwords do not match",  "Confirm_pass")
            is_valid = False
        return is_valid