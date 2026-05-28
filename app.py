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


# Helper functions for matching logic
def normalise_words(text):
    if text is None:
        return set()

    cleaned_text = text.lower().replace(",", " ")
    return set(cleaned_text.split())


def calculate_job_match(candidate, job):
    score = 0
    reasons = []

    candidate_skills = normalise_words(candidate["skills"])
    job_skills = normalise_words(job["required_skills"])

    matching_skills = candidate_skills.intersection(job_skills)

    if matching_skills:
        score += 40
        reasons.append("Skills match: " + ", ".join(sorted(matching_skills)))

    if candidate["preferred_work_mode"] == job["work_mode"]:
        score += 20
        reasons.append("Preferred work mode matches the job work mode.")

    candidate_location = (candidate["preferred_location"] or "").lower()
    job_location = (job["job_location"] or "").lower()

    if candidate_location and candidate_location in job_location:
        score += 15
        reasons.append("Preferred location matches the job location.")

    candidate_major = (candidate["major"] or "").lower()
    required_education = (job["required_education"] or "").lower()

    if candidate_major and candidate_major in required_education:
        score += 15
        reasons.append("Candidate major matches the required education field.")

    candidate_experience = candidate["years_experience"] or 0
    required_experience = job["years_experience_required"] or 0

    if candidate_experience >= required_experience:
        score += 10
        reasons.append("Candidate experience meets or exceeds the requirement.")

    if not reasons:
        reasons.append("This job has limited direct profile matches, but is still available for review.")

    return min(score, 100), reasons


# Helper function to match a candidate to a job (for employer view)
def calculate_candidate_match(candidate, job):
    score = 0
    reasons = []

    candidate_skills = normalise_words(candidate["skills"])
    job_skills = normalise_words(job["required_skills"])

    matching_skills = candidate_skills.intersection(job_skills)

    if matching_skills:
        score += 40
        reasons.append("Skills match: " + ", ".join(sorted(matching_skills)))

    if candidate["preferred_work_mode"] == job["work_mode"]:
        score += 20
        reasons.append("Candidate preferred work mode matches the job work mode.")

    candidate_location = (candidate["preferred_location"] or "").lower()
    job_location = (job["job_location"] or "").lower()

    if candidate_location and candidate_location in job_location:
        score += 15
        reasons.append("Candidate preferred location matches the job location.")

    candidate_major = (candidate["major"] or "").lower()
    required_education = (job["required_education"] or "").lower()

    if candidate_major and candidate_major in required_education:
        score += 15
        reasons.append("Candidate major matches the job education requirement.")

    candidate_experience = candidate["years_experience"] or 0
    required_experience = job["years_experience_required"] or 0

    if candidate_experience >= required_experience:
        score += 10
        reasons.append("Candidate experience meets or exceeds the job requirement.")

    if not reasons:
        reasons.append("This candidate has limited direct matches, but may still be worth reviewing.")

    return min(score, 100), reasons


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


# Candidate listing route for employers
@app.route("/candidates")
def candidate_list():
    if session.get("role") != "employer":
        return redirect(url_for("login"))

    db = get_db()

    keyword = request.args.get("keyword", "").strip()
    major = request.args.get("major", "").strip()
    preferred_location = request.args.get("preferred_location", "").strip()
    preferred_work_mode = request.args.get("preferred_work_mode", "").strip()

    query = """
        SELECT candidates.*, users.email
        FROM candidates
        JOIN users ON candidates.user_id = users.user_id
        WHERE 1 = 1
    """
    params = []

    if keyword:
        query += """
            AND (
                candidates.full_name LIKE ?
                OR candidates.education LIKE ?
                OR candidates.work_experience LIKE ?
                OR candidates.skills LIKE ?
                OR users.email LIKE ?
            )
        """
        keyword_search = f"%{keyword}%"
        params.extend([
            keyword_search,
            keyword_search,
            keyword_search,
            keyword_search,
            keyword_search
        ])

    if major:
        query += " AND candidates.major LIKE ?"
        params.append(f"%{major}%")

    if preferred_location:
        query += " AND candidates.preferred_location LIKE ?"
        params.append(f"%{preferred_location}%")

    if preferred_work_mode:
        query += " AND candidates.preferred_work_mode = ?"
        params.append(preferred_work_mode)

    query += " ORDER BY candidates.candidate_id DESC"

    candidates = db.execute(query, params).fetchall()

    return render_template(
        "candidate_list.html",
        candidates=candidates,
        keyword=keyword,
        major=major,
        preferred_location=preferred_location,
        preferred_work_mode=preferred_work_mode
    )


# Recommended jobs route for candidates
@app.route("/jobs/recommended")
def recommended_jobs():
    if session.get("role") != "candidate":
        return redirect(url_for("login"))

    db = get_db()
    user_id = session["user_id"]

    candidate = db.execute(
        "SELECT * FROM candidates WHERE user_id = ?",
        (user_id,)
    ).fetchone()

    if candidate is None:
        return "Please create a candidate profile before viewing recommended jobs."

    jobs = db.execute(
        """
        SELECT jobs.*, companies.company_name
        FROM jobs
        JOIN companies ON jobs.company_id = companies.company_id
        """
    ).fetchall()

    recommendations = []

    for job in jobs:
        score, reasons = calculate_job_match(candidate, job)
        recommendations.append({
            "job": job,
            "score": score,
            "reasons": reasons
        })

    recommendations.sort(key=lambda item: item["score"], reverse=True)

    if session.get("membership_status") != "member":
        recommendations = recommendations[:10]

    return render_template("recommended_jobs.html", recommendations=recommendations)

# Recommended candidates route for employers
@app.route("/candidates/recommended")
def recommended_candidates():
    if session.get("role") != "employer":
        return redirect(url_for("login"))

    db = get_db()
    user_id = session["user_id"]

    company = db.execute(
        "SELECT * FROM companies WHERE user_id = ?",
        (user_id,)
    ).fetchone()

    if company is None:
        return "Please create a company profile before viewing recommended candidates."

    jobs = db.execute(
        "SELECT * FROM jobs WHERE company_id = ?",
        (company["company_id"],)
    ).fetchall()

    if not jobs:
        return "Please create at least one job posting before viewing recommended candidates."

    candidates = db.execute(
        """
        SELECT candidates.*, users.email
        FROM candidates
        JOIN users ON candidates.user_id = users.user_id
        """
    ).fetchall()

    recommendations = []

    for candidate in candidates:
        best_score = 0
        best_reasons = []
        best_job = None

        for job in jobs:
            score, reasons = calculate_candidate_match(candidate, job)

            if score > best_score:
                best_score = score
                best_reasons = reasons
                best_job = job

        if best_job is not None:
            recommendations.append({
                "candidate": candidate,
                "job": best_job,
                "score": best_score,
                "reasons": best_reasons
            })

    recommendations.sort(key=lambda item: item["score"], reverse=True)

    if session.get("membership_status") != "member":
        recommendations = recommendations[:10]

    return render_template("recommended_candidates.html", recommendations=recommendations)

if __name__ == "__main__":
    if not os.path.exists(DATABASE):
        with app.app_context():
            init_db()
    app.run(debug=True)