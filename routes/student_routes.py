from flask import Blueprint, render_template, request, redirect, session, flash
from database.db import complaints_collection
from models.complaint_model import create_complaint
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from flask import current_app
from models.user_model import find_user_by_id, update_user
from bson import ObjectId
student_bp = Blueprint("student", __name__)

UPLOAD_FOLDER = "static/uploads"


@student_bp.route("/student")
def student_dashboard():
    return render_template("student/dashboard.html")


@student_bp.route("/student/new-complaint", methods=["GET", "POST"])
def new_complaint():
    if session.get("role") != "student":
        return redirect("/")

    if request.method == "POST":

        # 🔹 SAFE FORM FETCHING (no crash)
        title = request.form.get("title")
        description = request.form.get("description")

        # 🔹 VALIDATION
        if not title or not description:
            flash("Title and Description are required!", "error")
            return redirect("/student/new-complaint")

        # 🔹 FILE UPLOAD
        file = request.files.get("file")
        filename = None

        if file and file.filename != "":
            filename = secure_filename(file.filename)

            upload_folder = os.path.join(current_app.root_path, "static", "uploads")
            os.makedirs(upload_folder, exist_ok=True)
            
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)

        # 🔹 SAVE TO DATABASE
        create_complaint(session["user_id"], title, description, filename)

        flash("Complaint submitted successfully!", "success")
        return redirect("/student/my-complaints")

    return render_template("student/new_complaint.html")


# ---------------- PROFILE ----------------

@student_bp.route("/student/profile", methods=["GET", "POST"])
def student_profile():
    user_id = session.get("user_id")
    user = find_user_by_id(user_id)

    if request.method == "POST":
        update_user(
            user_id,
            request.form.get("name"),
            request.form.get("department")
        )
        flash("Profile updated!", "success")
        return redirect("/student/profile")

    return render_template("student/profile.html", user=user)


# ---------------- MY COMPLAINTS ----------------
@student_bp.route("/student/my-complaints")
def my_complaints():
    complaints = list(
        complaints_collection.find({"student_id": session["user_id"]})
    )
    return render_template(
        "student/my_complaints.html",
        complaints=complaints
    )
