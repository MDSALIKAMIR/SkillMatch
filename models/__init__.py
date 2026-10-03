from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


# ==========================
# USERS
# ==========================
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.Enum('student', 'admin', name='user_role'), default='student', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    profile = db.relationship('StudentProfile', backref='user', uselist=False, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'


# ==========================
# STUDENT PROFILE
# ==========================
class StudentProfile(db.Model):
    __tablename__ = 'student_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    college = db.Column(db.String(200))
    course = db.Column(db.String(150))
    graduation_year = db.Column(db.Integer)
    cgpa = db.Column(db.Numeric(4, 2))
    location = db.Column(db.String(150))
    looking_for = db.Column(db.Enum('Internship', 'Job', 'Both', name='looking_for_enum'), default='Both')
    expected_stipend = db.Column(db.Integer, default=0)
    expected_salary = db.Column(db.Integer, default=0)
    preferred_location = db.Column(db.String(150))
    work_mode = db.Column(db.Enum('Remote', 'Hybrid', 'On-site', 'Any', name='work_mode_enum'), default='Any')
    availability = db.Column(db.String(100))
    resume_path = db.Column(db.String(255))
    github = db.Column(db.String(255))
    linkedin = db.Column(db.String(255))
    portfolio = db.Column(db.String(255))

    skills = db.relationship('Skill', secondary='student_skills', backref='students')
    projects = db.relationship('Project', backref='student', cascade='all, delete-orphan')
    saved = db.relationship('SavedOpportunity', backref='student', cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='student', cascade='all, delete-orphan')

    def skill_names(self):
        return {s.skill_name.lower() for s in self.skills}


# ==========================
# SKILLS
# ==========================
class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(100), unique=True, nullable=False)


student_skills = db.Table(
    'student_skills',
    db.Column('student_id', db.Integer, db.ForeignKey('student_profiles.id', ondelete='CASCADE'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skills.id', ondelete='CASCADE'), primary_key=True),
    extend_existing=True
)


# ==========================
# PROJECTS
# ==========================
class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False)
    project_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    technologies = db.Column(db.String(255))
    github_url = db.Column(db.String(255))
    live_url = db.Column(db.String(255))


# ==========================
# COMPANIES
# ==========================
class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), nullable=False)
    logo = db.Column(db.String(255))
    website = db.Column(db.String(255))
    is_verified = db.Column(db.Boolean, default=False)

    opportunities = db.relationship('Opportunity', backref='company', cascade='all, delete-orphan')


# ==========================
# OPPORTUNITIES
# ==========================
class Opportunity(db.Model):
    __tablename__ = 'opportunities'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    type = db.Column(db.Enum('Internship', 'Full-time Job', 'Part-time', 'Apprenticeship', name='opp_type_enum'), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(150))
    work_mode = db.Column(db.Enum('Remote', 'Hybrid', 'On-site', name='opp_work_mode_enum'), default='On-site')
    stipend = db.Column(db.Integer, default=0)
    salary = db.Column(db.Integer, default=0)
    education_requirement = db.Column(db.String(150))
    experience_requirement = db.Column(db.String(150))
    deadline = db.Column(db.Date)
    apply_url = db.Column(db.String(500), nullable=False)
    is_sample = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    skills = db.relationship('Skill', secondary='opportunity_skills', backref='opportunities')

    def required_skill_names(self):
        return {s.skill_name.lower() for s in self.skills}


opportunity_skills = db.Table(
    'opportunity_skills',
    db.Column('opportunity_id', db.Integer, db.ForeignKey('opportunities.id', ondelete='CASCADE'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skills.id', ondelete='CASCADE'), primary_key=True),
    extend_existing=True
)


# ==========================
# SAVED OPPORTUNITIES
# ==========================
class SavedOpportunity(db.Model):
    __tablename__ = 'saved_opportunities'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id', ondelete='CASCADE'), nullable=False)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)

    opportunity = db.relationship('Opportunity')

    __table_args__ = (db.UniqueConstraint('student_id', 'opportunity_id', name='unique_save'),)


# ==========================
# APPLICATIONS
# ==========================
class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id', ondelete='CASCADE'), nullable=False)
    applied_date = db.Column(db.Date)
    status = db.Column(
        db.Enum('Saved', 'Applied', 'Shortlisted', 'Interview', 'Selected', 'Rejected', name='app_status_enum'),
        default='Saved'
    )
    notes = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    opportunity = db.relationship('Opportunity')
