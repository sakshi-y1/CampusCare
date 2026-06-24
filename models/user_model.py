from database.db import users_collection
from werkzeug.security import generate_password_hash
from bson import ObjectId


# ==============================
# CREATE USER (STUDENT / STAFF)
# ==============================
def create_user(name, email, password, role, department=None):
    users_collection.insert_one({
        "name": name,
        "email": email,
        "password": generate_password_hash(password),  # hashed
        "role": role,
        "department": department
    })


# ==============================
# FIND USER BY EMAIL
# ==============================
def find_user(email):
    return users_collection.find_one({"email": email})


# ==============================
# FIND USER BY ID
# ==============================
def find_user_by_id(user_id):
    return users_collection.find_one({"_id": ObjectId(user_id)})


# ==============================
# UPDATE USER PROFILE
# ==============================
def update_user(user_id, name, department):
    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {
            "name": name,
            "department": department
        }}
    )
