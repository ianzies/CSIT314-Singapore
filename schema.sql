DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS candidates;
DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS jobs;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('candidate', 'employer')),
    membership_status TEXT NOT NULL DEFAULT 'non_member'
        CHECK(membership_status IN ('member', 'non_member'))
);

CREATE TABLE candidates (
    candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    full_name TEXT NOT NULL,
    contact_info TEXT,
    education TEXT,
    major TEXT,
    years_experience INTEGER DEFAULT 0,
    work_experience TEXT,
    skills TEXT,
    preferred_work_mode TEXT,
    preferred_location TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE companies (
    company_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    company_name TEXT NOT NULL,
    company_description TEXT,
    industry TEXT,
    location TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE jobs (
    job_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    job_title TEXT NOT NULL,
    job_description TEXT,
    required_education TEXT,
    required_skills TEXT,
    years_experience_required INTEGER DEFAULT 0,
    work_mode TEXT,
    job_location TEXT,
    salary_range TEXT,
    job_type TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);