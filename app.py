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


# Company profile route
@app.route("/company/profile", methods=["GET", "POST"])
def company_profile():
    if session.get("role") != "employer":
        return redirect(url_for("login"))

    db = get_db()
    user_id = session["user_id"]

    company = db.execute(
        "SELECT * FROM companies WHERE user_id = ?",
        (user_id,)
    ).fetchone()

    if request.method == "POST":
        company_name = request.form["company_name"]
        company_description = request.form["company_description"]
        industry = request.form["industry"]
        location = request.form["location"]

        if company:
            db.execute(
                """
                UPDATE companies
                SET company_name = ?, company_description = ?, industry = ?, location = ?
                WHERE user_id = ?
                """,
                (company_name, company_description, industry, location, user_id)
            )
        else:
            db.execute(
                """
                INSERT INTO companies (
                    user_id, company_name, company_description, industry, location
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, company_name, company_description, industry, location)
            )

        db.commit()
        return redirect(url_for("employer_dashboard"))

    return render_template("company_profile.html", company=company)


# Job creation route
@app.route("/jobs/create", methods=["GET", "POST"])
def create_job():
    if session.get("role") != "employer":
        return redirect(url_for("login"))

    db = get_db()
    user_id = session["user_id"]

    company = db.execute(
        "SELECT * FROM companies WHERE user_id = ?",
        (user_id,)
    ).fetchone()

    if company is None:
        return "Please create a company profile before posting jobs."

    if request.method == "POST":
        job_title = request.form["job_title"]
        job_description = request.form["job_description"]
        required_education = request.form["required_education"]
        required_skills = request.form["required_skills"]
        years_experience_required = request.form["years_experience_required"]
        work_mode = request.form["work_mode"]
        job_location = request.form["job_location"]
        salary_range = request.form["salary_range"]
        job_type = request.form["job_type"]

        db.execute(
            """
            INSERT INTO jobs (
                company_id, job_title, job_description, required_education,
                required_skills, years_experience_required, work_mode,
                job_location, salary_range, job_type
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                company["company_id"], job_title, job_description,
                required_education, required_skills, years_experience_required,
                work_mode, job_location, salary_range, job_type
            )
        )

        db.commit()
        return redirect(url_for("employer_dashboard"))

    return render_template("job_form.html")


# Job listing route for candidates
@app.route("/jobs")
def job_list():
    if session.get("role") != "candidate":
        return redirect(url_for("login"))

    db = get_db()

    keyword = request.args.get("keyword", "").strip()
    location = request.args.get("location", "").strip()
    work_mode = request.args.get("work_mode", "").strip()
    job_type = request.args.get("job_type", "").strip()

    query = """
        SELECT jobs.*, companies.company_name
        FROM jobs
        JOIN companies ON jobs.company_id = companies.company_id
        WHERE 1 = 1
    """
    params = []

    if keyword:
        query += """
            AND (
                jobs.job_title LIKE ?
                OR jobs.job_description LIKE ?
                OR jobs.required_skills LIKE ?
                OR companies.company_name LIKE ?
            )
        """
        keyword_search = f"%{keyword}%"
        params.extend([keyword_search, keyword_search, keyword_search, keyword_search])

    if location:
        query += " AND jobs.job_location LIKE ?"
        params.append(f"%{location}%")

    if work_mode:
        query += " AND jobs.work_mode = ?"
        params.append(work_mode)

    if job_type:
        query += " AND jobs.job_type = ?"
        params.append(job_type)

    query += " ORDER BY jobs.job_id DESC"

    jobs = db.execute(query, params).fetchall()

    return render_template(
        "job_list.html",
        jobs=jobs,
        keyword=keyword,
        location=location,
        work_mode=work_mode,
        job_type=job_type
    )


if __name__ == "__main__":
    if not os.path.exists(DATABASE):
        with app.app_context():
            init_db()
    app.run(debug=True)