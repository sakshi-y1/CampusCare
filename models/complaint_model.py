from database.db import complaints_collection
from datetime import datetime
from bson import ObjectId


# ==============================
# STUDENT: CREATE COMPLAINT
# ==============================
def create_complaint(student_id, title, description, filename=None):
    complaints_collection.insert_one({
        "student_id": student_id,
        "title": title,
        "description": description,
        "file": filename, 
        "status": "Pending",
        "department": None,          # assigned later by admin
        "created_at": datetime.now(),
        "updated_at": None
    })


# ==============================
# ADMIN: VIEW ALL COMPLAINTS
# ==============================
def get_all_complaints(query={}):
    return complaints_collection.find(query)


# ==============================
# ADMIN: ASSIGN DEPARTMENT
# ==============================
def assign_department(complaint_id, department):
    complaints_collection.update_one(
        {"_id": ObjectId(complaint_id)},
        {"$set": {
            "department": department,
            "status": "Assigned",
            "updated_at": datetime.now()
        }}
    )


# ==============================
# STAFF: VIEW COMPLAINTS BY DEPARTMENT (STEP 8)
# ==============================
def get_complaints_by_department(department):
    """
    Returns only complaints that:
    - are assigned
    - belong to the logged-in staff's department
    """
    return complaints_collection.find({
        "department": department,
        "status": {"$in": ["Assigned", "In Progress", "Resolved"]}
    })


# ==============================
# STAFF: UPDATE COMPLAINT STATUS
# ==============================
def update_complaint_status(complaint_id, status):
    complaints_collection.update_one(
        {"_id": ObjectId(complaint_id)},
        {"$set": {
            "status": status,
            "updated_at": datetime.now()
        }}
    )
