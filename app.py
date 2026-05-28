from flask import Flask, render_template, request, redirect, session, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "replace-this-with-a-secret-key"

DATABASE = "database.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with open("schema.sql", "r") as f:
        db.executescript(f.read())
    db.commit()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]
        membership_status = request.form["membership_status"]

        password_hash = generate_password_hash(password)

        db = get_db()

        try:
            db.execute(
                """
                INSERT INTO users (email, password_hash, role, membership_status)
                VALUES (?, ?, ?, ?)
                """,
                (email, password_hash, role, membership_status)
            )
            db.commit()
        except sqlite3.IntegrityError:
            return "Email already registered."

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        if user is None or not check_password_hash(user["password_hash"], password):
            return "Invalid email or password."

        session["user_id"] = user["user_id"]
        session["role"] = user["role"]
        session["membership_status"] = user["membership_status"]

        if user["role"] == "candidate":
            return redirect(url_for("candidate_dashboard"))
        else:
            return redirect(url_for("employer_dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/candidate/dashboard")
def candidate_dashboard():
    if session.get("role") != "candidate":
        return redirect(url_for("login"))

    return render_template("candidate_dashboard.html")


# Candidate profile route
@app.route("/candidate/profile", methods=["GET", "POST"])
def candidate_profile():
    if session.get("role") != "candidate":
        return redirect(url_for("login"))

    db = get_db()
    user_id = session["user_id"]

    profile = db.execute(
        "SELECT * FROM candidates WHERE user_id = ?",
        (user_id,)
    ).fetchone()

    if request.method == "POST":
        full_name = request.form["full_name"]
        contact_info = request.form["contact_info"]
        education = request.form["education"]
        major = request.form["major"]
        years_experience = request.form["years_experience"]
        work_experience = request.form["work_experience"]
        skills = request.form["skills"]
        preferred_work_mode = request.form["preferred_work_mode"]
        preferred_location = request.form["preferred_location"]

        if profile:
            db.execute(
                """
                UPDATE candidates
                SET full_name = ?, contact_info = ?, education = ?, major = ?,
                    years_experience = ?, work_experience = ?, skills = ?,
                    preferred_work_mode = ?, preferred_location = ?
                WHERE user_id = ?
                """,
                (
                    full_name, contact_info, education, major,
                    years_experience, work_experience, skills,
                    preferred_work_mode, preferred_location, user_id
                )
            )
        else:
            db.execute(
                """
                INSERT INTO candidates (
                    user_id, full_name, contact_info, education, major,
                    years_experience, work_experience, skills,
                    preferred_work_mode, preferred_location
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id, full_name, contact_info, education, major,
                    years_experience, work_experience, skills,
                    preferred_work_mode, preferred_location
                )
            )

        db.commit()
        return redirect(url_for("candidate_dashboard"))

    return render_template("candidate_profile.html", profile=profile)


@app.route("/employer/dashboard")
def employer_dashboard():
    if session.get("role") != "employer":
        return redirect(url_for("login"))

    return render_template("employer_dashboard.html")


if __name__ == "__main__":
    if not os.path.exists(DATABASE):
        with app.app_context():
            init_db()
    app.run(debug=True)