from flask import Flask, jsonify
from config import SECRET_KEY, MONGO_URI
from routes.auth_routes import auth_bp
from routes.student_routes import student_bp
from routes.admin_routes import admin_bp
from routes.staff_routes import staff_bp
from database.mongo import mongo
from routes.admin_routes import admin_bp


app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config["MONGO_URI"] = "mongodb://localhost:27017/campuscare"

mongo.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(staff_bp)


if __name__ == "__main__":
    app.run(debug=True)
