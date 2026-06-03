import os
import sqlite3
from werkzeug.security import generate_password_hash


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR) if os.path.basename(CURRENT_DIR) == "static" else CURRENT_DIR
DATABASE_PATH = os.path.join(PROJECT_ROOT, "database.db")
SCHEMA_PATH = os.path.join(PROJECT_ROOT, "schema.sql")
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "uploads", "resumes")

DEMO_PASSWORD = "Password123!"
PASSWORD_HASH = generate_password_hash(DEMO_PASSWORD)


USERS = [
    ("candidate.member@align.test", PASSWORD_HASH, "candidate", "member"),
    ("candidate.free@align.test", PASSWORD_HASH, "candidate", "non_member"),
    ("employer.member@align.test", PASSWORD_HASH, "employer", "member"),
    ("employer.free@align.test", PASSWORD_HASH, "employer", "non_member"),
    ("maya.chen@align.test", PASSWORD_HASH, "candidate", "member"),
    ("liam.patel@align.test", PASSWORD_HASH, "candidate", "non_member"),
    ("sofia.nguyen@align.test", PASSWORD_HASH, "candidate", "member"),
    ("noah.kim@align.test", PASSWORD_HASH, "candidate", "non_member"),
    ("ava.singh@align.test", PASSWORD_HASH, "candidate", "member"),
    ("ethan.tan@align.test", PASSWORD_HASH, "candidate", "non_member"),
    ("olivia.wong@align.test", PASSWORD_HASH, "candidate", "member"),
    ("jack.lim@align.test", PASSWORD_HASH, "candidate", "non_member"),
    ("mia.park@align.test", PASSWORD_HASH, "candidate", "member"),
    ("lucas.ong@align.test", PASSWORD_HASH, "candidate", "non_member"),
    ("northstar.hr@align.test", PASSWORD_HASH, "employer", "member"),
    ("greenbyte.hr@align.test", PASSWORD_HASH, "employer", "member"),
    ("cloudbridge.hr@align.test", PASSWORD_HASH, "employer", "non_member"),
    ("securewave.hr@align.test", PASSWORD_HASH, "employer", "member"),
]


CANDIDATES = {
    "candidate.member@align.test": (
        "Alex Morgan", "alex.morgan@example.com | +61 400 100 001", "Bachelor", "Computer Science", 3,
        "Built Flask dashboards, automated SQL reports, and supported machine learning prototypes for business teams.",
        "Python, SQL, Flask, machine learning, data analysis, pandas", "Hybrid", "Sydney",
        "alex_morgan_resume.pdf", 1
    ),
    "candidate.free@align.test": (
        "Jamie Lee", "jamie.lee@example.com | +61 400 100 002", "Diploma", "Information Technology", 1,
        "Assisted with web application testing, documentation, and frontend bug fixing.",
        "HTML, CSS, JavaScript, testing, documentation", "Remote", "Sydney",
        None, 0
    ),
    "maya.chen@align.test": (
        "Maya Chen", "maya.chen@example.com | +61 400 100 003", "Master", "Artificial Intelligence", 5,
        "Developed recommendation models, NLP classifiers, and Python data pipelines for product analytics.",
        "Python, machine learning, AI, NLP, TensorFlow, data mining", "Remote", "Melbourne",
        "maya_chen_resume.pdf", 1
    ),
    "liam.patel@align.test": (
        "Liam Patel", "liam.patel@example.com | +61 400 100 004", "Bachelor", "Cybersecurity", 4,
        "Performed vulnerability assessments, incident response documentation, and network security monitoring.",
        "cybersecurity, information security, SIEM, incident response, Python, Linux", "Hybrid", "Canberra",
        "liam_patel_resume.pdf", 1
    ),
    "sofia.nguyen@align.test": (
        "Sofia Nguyen", "sofia.nguyen@example.com | +61 400 100 005", "Bachelor", "Software Engineering", 2,
        "Built frontend components and REST API integrations for recruitment and education platforms.",
        "JavaScript, React, HTML, CSS, frontend, API, Git", "Hybrid", "Sydney",
        None, 0
    ),
    "noah.kim@align.test": (
        "Noah Kim", "noah.kim@example.com | +61 400 100 006", "Master", "Data Science", 6,
        "Led analytics projects using SQL, Python, dashboards, and predictive models for customer insights.",
        "Python, SQL, data analytics, dashboards, pandas, Power BI, machine learning", "On-site", "Sydney",
        "noah_kim_resume.pdf", 1
    ),
    "ava.singh@align.test": (
        "Ava Singh", "ava.singh@example.com | +61 400 100 007", "Doctorate", "Computer Science", 7,
        "Researched graph-based recommender systems and deployed ranking experiments for search products.",
        "Python, recommendation systems, machine learning, NLP, data mining, research", "Remote", "Brisbane",
        "ava_singh_resume.pdf", 1
    ),
    "ethan.tan@align.test": (
        "Ethan Tan", "ethan.tan@example.com | +61 400 100 008", "Bachelor", "Information Systems", 2,
        "Maintained cloud support scripts, wrote API tests, and supported database migration tasks.",
        "Python, SQL, API, cloud, testing, backend", "Remote", "Melbourne",
        None, 0
    ),
    "olivia.wong@align.test": (
        "Olivia Wong", "olivia.wong@example.com | +61 400 100 009", "Bachelor", "Cybersecurity", 3,
        "Worked on secure coding reviews, phishing awareness dashboards, and access control checks.",
        "cybersecurity, secure coding, Python, SQL, access control, risk assessment", "Hybrid", "Sydney",
        "olivia_wong_resume.pdf", 1
    ),
    "jack.lim@align.test": (
        "Jack Lim", "jack.lim@example.com | +61 400 100 010", "Diploma", "Web Development", 1,
        "Created responsive web pages, fixed CSS layout bugs, and helped test Flask prototype features.",
        "HTML, CSS, JavaScript, Flask, frontend, testing", "On-site", "Wollongong",
        None, 0
    ),
    "mia.park@align.test": (
        "Mia Park", "mia.park@example.com | +61 400 100 011", "Master", "Business Analytics", 4,
        "Built reporting dashboards and data visualisation workflows for operations teams.",
        "SQL, Python, data visualisation, analytics, Tableau, pandas", "Hybrid", "Sydney",
        "mia_park_resume.pdf", 1
    ),
    "lucas.ong@align.test": (
        "Lucas Ong", "lucas.ong@example.com | +61 400 100 012", "Bachelor", "Computer Science", 3,
        "Implemented backend endpoints, authentication flows, and database-backed web features.",
        "Python, Flask, backend, SQL, API, authentication", "Remote", "Canberra",
        None, 0
    ),
}


COMPANIES = {
    "employer.member@align.test": (
        "DemoTech Hiring", "Technology", "Sydney",
        "DemoTech Hiring uses structured candidate matching to recruit junior and mid-level technology talent."
    ),
    "employer.free@align.test": (
        "Starter Labs", "Software", "Melbourne",
        "Starter Labs is a small software company testing candidate search and recommendation workflows."
    ),
    "northstar.hr@align.test": (
        "Northstar Analytics", "Data Analytics", "Sydney",
        "Northstar Analytics builds dashboards, reporting tools, and data products for business teams."
    ),
    "greenbyte.hr@align.test": (
        "GreenByte Systems", "Clean Technology", "Canberra",
        "GreenByte Systems creates optimisation software for energy and sustainability products."
    ),
    "cloudbridge.hr@align.test": (
        "CloudBridge Digital", "Cloud Services", "Melbourne",
        "CloudBridge Digital provides cloud migration, API integration, and platform support services."
    ),
    "securewave.hr@align.test": (
        "SecureWave Consulting", "Cybersecurity", "Sydney",
        "SecureWave Consulting supports organisations with incident response, secure coding, and risk assessment."
    ),
}


JOBS = [
    ("employer.member@align.test", "Junior Python Developer", "Build and maintain Flask web features for internal recruitment tools.", "Bachelor", "Python, Flask, SQL, backend, API", 1, "Hybrid", "Sydney", "$60,000 - $70,000", "Full-time"),
    ("employer.member@align.test", "Frontend Web Assistant", "Assist with responsive interface updates, CSS fixes, and JavaScript interactions.", "Diploma", "HTML, CSS, JavaScript, frontend, testing", 1, "Remote", "Sydney", "$50,000 - $60,000", "Part-time"),
    ("northstar.hr@align.test", "Junior Data Analyst", "Analyse datasets, build reports, and help create dashboards for business clients.", "Bachelor", "Python, SQL, pandas, data visualisation", 1, "Hybrid", "Sydney", "$65,000 - $80,000", "Full-time"),
    ("northstar.hr@align.test", "Business Intelligence Analyst", "Create executive dashboards and automate reporting pipelines for analytics teams.", "Bachelor", "SQL, Python, analytics, Tableau, Power BI", 3, "Hybrid", "Sydney", "$80,000 - $100,000", "Full-time"),
    ("greenbyte.hr@align.test", "AI Recommendation Researcher", "Prototype recommendation systems for energy optimisation products.", "Doctorate", "Python, recommendation systems, machine learning, NLP, data mining", 4, "Remote", "Canberra", "$110,000 - $140,000", "Full-time"),
    ("greenbyte.hr@align.test", "Machine Learning Engineer", "Develop machine learning workflows and ranking models for clean technology applications.", "Master", "Python, machine learning, TensorFlow, data mining, AI", 3, "Remote", "Melbourne", "$100,000 - $120,000", "Full-time"),
    ("cloudbridge.hr@align.test", "Backend API Developer", "Build API integrations, backend services, and SQL-backed workflow tools.", "Bachelor", "Python, Flask, API, SQL, backend", 2, "Remote", "Melbourne", "$80,000 - $100,000", "Contract"),
    ("cloudbridge.hr@align.test", "Cloud Support Analyst", "Support cloud migration testing, documentation, and database troubleshooting.", "Diploma", "cloud, SQL, testing, documentation, API", 1, "Hybrid", "Melbourne", "$60,000 - $70,000", "Full-time"),
    ("securewave.hr@align.test", "Cybersecurity Analyst", "Monitor security alerts, support incident response, and document risk findings.", "Bachelor", "cybersecurity, SIEM, incident response, Python, Linux", 2, "Hybrid", "Sydney", "$80,000 - $100,000", "Full-time"),
    ("securewave.hr@align.test", "Secure Coding Reviewer", "Review application code, identify security weaknesses, and support secure development practices.", "Bachelor", "cybersecurity, secure coding, Python, access control, risk assessment", 3, "Remote", "Sydney", "$100,000 - $120,000", "Full-time"),
    ("employer.free@align.test", "Software Testing Intern", "Test web application features and document bugs for a small software team.", "Diploma", "testing, documentation, HTML, CSS, JavaScript", 0, "On-site", "Melbourne", "$40,000 - $50,000", "Internship"),
    ("employer.free@align.test", "Graduate Software Assistant", "Assist with basic web app testing, documentation, and small Flask updates.", "Bachelor", "Python, Flask, HTML, CSS", 1, "Remote", "Sydney", "$50,000 - $60,000", "Part-time"),
]


def reset_database():
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    with sqlite3.connect(DATABASE_PATH) as conn:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
            conn.executescript(schema_file.read())
        conn.commit()


def insert_users(conn):
    cursor = conn.cursor()
    user_ids = {}

    for email, password_hash, role, membership_status in USERS:
        cursor.execute(
            """
            INSERT INTO users (email, password_hash, role, membership_status)
            VALUES (?, ?, ?, ?)
            """,
            (email, password_hash, role, membership_status)
        )
        user_ids[email] = cursor.lastrowid

    return user_ids


def insert_candidates(conn, user_ids):
    cursor = conn.cursor()

    for email, candidate in CANDIDATES.items():
        (
            full_name, contact_info, education, major, years_experience,
            work_experience, skills, preferred_work_mode, preferred_location,
            resume_filename, resume_visible_to_employers
        ) = candidate

        cursor.execute(
            """
            INSERT INTO candidates (
                user_id, full_name, contact_info, education, major,
                years_experience, work_experience, skills,
                preferred_work_mode, preferred_location, resume_filename,
                resume_visible_to_employers
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_ids[email], full_name, contact_info, education, major,
                years_experience, work_experience, skills,
                preferred_work_mode, preferred_location, resume_filename,
                resume_visible_to_employers
            )
        )


def insert_companies(conn, user_ids):
    cursor = conn.cursor()
    company_ids = {}

    for email, company in COMPANIES.items():
        company_name, industry, location, company_description = company

        cursor.execute(
            """
            INSERT INTO companies (user_id, company_name, industry, location, company_description)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_ids[email], company_name, industry, location, company_description)
        )
        company_ids[email] = cursor.lastrowid

    return company_ids


def insert_jobs(conn, company_ids):
    cursor = conn.cursor()

    for job in JOBS:
        (
            employer_email, job_title, job_description, required_education,
            required_skills, years_experience_required, work_mode, job_location,
            salary_range, job_type
        ) = job

        cursor.execute(
            """
            INSERT INTO jobs (
                company_id, job_title, job_description, required_education,
                required_skills, years_experience_required, work_mode,
                job_location, salary_range, job_type
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                company_ids[employer_email], job_title, job_description,
                required_education, required_skills, years_experience_required,
                work_mode, job_location, salary_range, job_type
            )
        )


def main():
    reset_database()

    with sqlite3.connect(DATABASE_PATH) as conn:
        user_ids = insert_users(conn)
        insert_candidates(conn, user_ids)
        company_ids = insert_companies(conn, user_ids)
        insert_jobs(conn, company_ids)
        conn.commit()

    print("Demo database created successfully.")
    print("Database:", DATABASE_PATH)
    print("\nDemo login accounts:")
    print("Candidate member:     candidate.member@align.test")
    print("Candidate non-member: candidate.free@align.test")
    print("Employer member:      employer.member@align.test")
    print("Employer non-member:  employer.free@align.test")
    print("Password for all:     Password123!")


if __name__ == "__main__":
    main()