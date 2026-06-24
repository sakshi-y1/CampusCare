from flask import Blueprint, render_template, request, redirect, session
from models.user_model import create_user, find_user
from werkzeug.security import check_password_hash

auth_bp = Blueprint("auth", __name__)


# =========================
# LOGIN
# =========================
@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = find_user(email)

        if user and check_password_hash(user["password"], password):

            # ✅ BASIC SESSION DATA
            session["user_id"] = str(user["_id"])
            session["role"] = user["role"]

            # ✅ IMPORTANT FIX: SAVE DEPARTMENT FOR STAFF
            if user["role"] == "staff":
                session["department"] = user.get("department")

            # =========================
            # ROLE BASED REDIRECTION
            # =========================
            if user["role"] == "admin":
                return redirect("/admin/complaints")

            elif user["role"] == "student":
                return redirect("/student")

            elif user["role"] == "staff":
                return redirect("/staff")

        return render_template(
            "auth/login.html",
            error="Invalid email or password"
        )

    return render_template("auth/login.html")


# =========================
# REGISTER (Student / Staff)
# =========================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        create_user(
            name=request.form["name"],
            email=request.form["email"],
            password=request.form["password"],
            role=request.form["role"],
            department=request.form.get("department")  # ✅ already correct
        )
        
        return redirect("/")

    return render_template("auth/register.html")


# =========================
# LOGOUT
# =========================
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
