from flask import Blueprint, render_template, session, redirect, request, url_for
from models.complaint_model import get_complaints_by_department, update_complaint_status
from models.user_model import find_user_by_id
from bson.objectid import ObjectId
from models.user_model import find_user_by_id
from database import db

staff_bp = Blueprint("staff", __name__)

@staff_bp.route("/staff")
def staff_dashboard():
    if session.get("role") != "staff":
        return redirect("/")

    # Get department from session
    department = session.get("department")

    # Safety check
    if not department:
        return "Department not assigned to staff", 403

    # Fetch ONLY that department complaints
    complaints_cursor = get_complaints_by_department(department)
    complaints = list(complaints_cursor)

    return render_template(
        "staff/dashboard.html",
        complaints=complaints,
        department=department
    )



@staff_bp.route("/staff/update-status/<complaint_id>", methods=["POST"])
def staff_update_status(complaint_id):
    # Security check again
    if session.get("role") != "staff":
        return redirect("/")

    # Get updated status from form
    status = request.form["status"]

    # Update complaint status in DB
    update_complaint_status(complaint_id, status)

    # Redirect back to staff dashboard
    return redirect("/staff")


@staff_bp.route("/staff/profile")
def staff_profile():

    # Check role
    if session.get("role") != "staff":
        return redirect("/")

    # Get logged in user id
    user_id = session.get("user_id")

    if not user_id:
        return redirect("/")

    # Fetch staff from DB
    staff = find_user_by_id(user_id)

    return render_template("staff/profile.html", staff=staff)

@staff_bp.route("/department-complaints")
def department_complaints():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    department = session["user"]["department"]

    complaints = db.complaints.find({"department": department})

    return render_template(
        "staff/department_complaints.html",
        complaints=complaints,
        department=department
    )
