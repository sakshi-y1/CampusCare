from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from models.complaint_model import get_all_complaints, assign_department, update_complaint_status
from database.db import complaints_collection
from flask import jsonify
from datetime import datetime, timedelta
from collections import defaultdict
from database.mongo import mongo
from collections import Counter



admin_bp = Blueprint("admin", __name__)

# =========================
# ADMIN DASHBOARD
# =========================
@admin_bp.route("/admin/complaints")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect("/")

    status = request.args.get("status")
    department = request.args.get("department")

    query = {}

    if status and status != "All":
        query["status"] = status

    if department and department != "All":
        query["department"] = department

    complaints = list(get_all_complaints(query))
    total = complaints_collection.count_documents({})
    pending = complaints_collection.count_documents({"status": "Pending"})
    assigned = complaints_collection.count_documents({"status": "Assigned"})
    progress = complaints_collection.count_documents({"status": "In Progress"})
    resolved = complaints_collection.count_documents({"status": "Resolved"})



    return render_template(
        "admin/complaints.html",
        complaints=complaints,
        selected_status=status,
        selected_department=department,
        total=total,
        pending=pending,
        assigned=assigned,
        progress=progress,
        resolved=resolved
    )



# =========================
# UPDATE STATUS (ADMIN)
# =========================
@admin_bp.route("/admin/update-status/<complaint_id>", methods=["POST"])
def update_status(complaint_id):
    if session.get("role") != "admin":
        return redirect("/")

    status = request.form.get("status")

    update_complaint_status(complaint_id, status)

    flash("Complaint status updated successfully ✅", "success")

    return redirect(url_for("admin.admin_dashboard"))


# =========================
# ASSIGN DEPARTMENT
# =========================
@admin_bp.route("/admin/assign/<complaint_id>", methods=["POST"])
def assign_complaint(complaint_id):
    if session.get("role") != "admin":
        return redirect("/")

    department = request.form.get("department")

    if not department:
        flash("Please select a department ⚠️", "error")
        return redirect(url_for("admin.admin_dashboard"))

    assign_department(complaint_id, department)

    flash(f"Complaint assigned to {department} successfully 🎉", "success")

    return redirect(url_for("admin.admin_dashboard"))





@admin_bp.route('/admin/complaint-analytics')
def complaint_analytics():
    
    complaints = mongo.db.complaints.find()

    dept_list = []
    status_list = []
    month_list = []

    for c in complaints:
        dept_list.append(c.get("department", "Unknown"))
        status_list.append(c.get("status", "Pending"))

        if "created_at" in c:
            month_list.append(c["created_at"].strftime("%B"))

    department_data = dict(Counter(dept_list))
    status_data = dict(Counter(status_list))
    monthly_data = dict(Counter(month_list))

    total_complaints = sum(department_data.values())

    return render_template(
        "admin/complaint_analytics.html",
        department_data=department_data,
        status_data=status_data,
        monthly_data=monthly_data,
        total_complaints=total_complaints
    )