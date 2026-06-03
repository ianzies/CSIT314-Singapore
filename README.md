# ALIGN Recruitment Platform

ALIGN is a recruitment platform developed for CSIT314. The system supports two main user roles: candidates and employers. Candidates can create structured profiles, browse job listings, and receive ranked job recommendations. Employers can create company profiles, post job listings, search candidates, and view ranked candidate recommendations.

The platform uses profile and job data such as skills, education level, experience, work mode, and location to support structured job matching. It also includes membership-based recommendation access and resume upload with candidate consent controls.

## Tech Stack

- Python
- Flask
- SQLite
- HTML
- CSS

## Setup Instructions

### 1. Clone the repository

bash git clone <repository-url> cd CSIT314-Singapore 

### 2. Create and activate a virtual environment

For macOS/Linux:

bash python3 -m venv .venv source .venv/bin/activate 

For Windows:

bash python -m venv .venv .venv\Scripts\activate 

### 3. Install dependencies

bash pip install -r requirements.txt 

### 4. Initialise the database

The project uses SQLite. If database.db does not already exist, the application will initialise the database from schema.sql when the app is first run.

bash python app.py 

### 5. Run the application

bash python app.py 

Then open the application in your browser:

text http://127.0.0.1:5000 

## Local Files Not Included in Git

The following files are intentionally ignored:

text database.db uploads/resumes/* static/seed_demo_data.py .DS_Store database_backup.db 

This keeps local databases, uploaded resumes, and demo-only files out of the submitted repository.

## Notes

This is a prototype system intended for academic demonstration. Resume files are stored locally for demonstration purposes, and uploaded resume access is restricted through candidate consent and employer membership checks.
