"""
One-command database initializer for local development.

This creates all tables via SQLAlchemy (equivalent to database/schema.sql),
then seeds skills/companies/opportunities (equivalent to database/seed.sql),
and creates a demo admin account.

Usage:
    python init_db.py

Make sure your MySQL server is running and the database in .env (DB_NAME)
already exists, e.g.:
    CREATE DATABASE skillmatch CHARACTER SET utf8mb4;
"""
from datetime import date
from app import create_app
from models import db, User, StudentProfile, Skill, Company, Opportunity

app = create_app()

SKILLS = [
    'Python', 'SQL', 'HTML', 'CSS', 'JavaScript', 'React', 'Node.js',
    'Flask', 'Django', 'Java', 'C++', 'Git', 'Docker', 'AWS',
    'Machine Learning', 'Data Analysis', 'MongoDB', 'MySQL', 'REST APIs',
    'Bootstrap', 'TypeScript', 'Linux', 'Cybersecurity Basics', 'Excel',
]

COMPANIES = [
    ('NovaTech Labs', 'https://example.com/novatech'),
    ('BrightPath Solutions', 'https://example.com/brightpath'),
    ('CloudNine Systems', 'https://example.com/cloudnine'),
    ('DataSphere Analytics', 'https://example.com/datasphere'),
    ('PixelForge Studios', 'https://example.com/pixelforge'),
    ('SecureNet Technologies', 'https://example.com/securenet'),
    ('GreenLeaf Fintech', 'https://example.com/greenleaf'),
    ('Orbit Commerce', 'https://example.com/orbit'),
    ('Quantum Byte', 'https://example.com/quantumbyte'),
    ('Skyline Ventures', 'https://example.com/skyline'),
]

# (company index, title, type, description, location, work_mode, stipend, salary,
#  edu, exp, deadline, apply_url, [skill names])
OPPORTUNITIES = [
    (0, 'Frontend Developer Intern', 'Internship', 'Work on React-based dashboards for our SaaS product.', 'Bangalore', 'Remote', 15000, 0, 'BCA/B.Tech', '0-1 years', date(2026, 11, 30), 'https://example.com/apply/novatech-frontend', ['HTML', 'CSS', 'JavaScript', 'React', 'Bootstrap']),
    (0, 'Backend Developer Intern', 'Internship', 'Build REST APIs using Python and Flask.', 'Bangalore', 'Hybrid', 18000, 0, 'BCA/B.Tech', '0-1 years', date(2026, 12, 5), 'https://example.com/apply/novatech-backend', ['Python', 'SQL', 'Flask', 'REST APIs']),
    (1, 'Full Stack Developer (Entry Level)', 'Full-time Job', 'Join our engineering team building MERN stack products.', 'Pune', 'On-site', 0, 480000, 'B.Tech/BCA', '0-2 years', date(2026, 11, 20), 'https://example.com/apply/brightpath-fullstack', ['JavaScript', 'React', 'Node.js', 'MongoDB', 'REST APIs']),
    (1, 'Junior QA Engineer', 'Full-time Job', 'Manual and automated testing for web applications.', 'Pune', 'Hybrid', 0, 350000, 'Any Graduate', '0-1 years', date(2026, 11, 25), 'https://example.com/apply/brightpath-qa', ['Python', 'Git', 'REST APIs']),
    (2, 'Cloud Support Intern', 'Internship', 'Assist with AWS infrastructure monitoring and support.', 'Hyderabad', 'Remote', 12000, 0, 'B.Tech/BCA', '0-1 years', date(2026, 12, 10), 'https://example.com/apply/cloudnine-support', ['AWS', 'Linux', 'Cybersecurity Basics']),
    (2, 'DevOps Intern', 'Internship', 'Work with Docker, CI/CD pipelines and deployment automation.', 'Hyderabad', 'On-site', 20000, 0, 'B.Tech/BCA', '0-1 years', date(2026, 12, 15), 'https://example.com/apply/cloudnine-devops', ['Docker', 'Linux', 'Cybersecurity Basics', 'Python']),
    (3, 'Data Analyst Intern', 'Internship', 'Analyze business data using SQL and Python.', 'Mumbai', 'Hybrid', 15000, 0, 'Any Graduate', '0-1 years', date(2026, 11, 28), 'https://example.com/apply/datasphere-analyst', ['Python', 'SQL', 'Excel']),
    (3, 'Machine Learning Intern', 'Internship', 'Build and evaluate ML models for prediction tasks.', 'Mumbai', 'Remote', 20000, 0, 'B.Tech/BCA/MCA', '0-1 years', date(2026, 12, 1), 'https://example.com/apply/datasphere-ml', ['Python', 'Machine Learning', 'REST APIs']),
    (4, 'UI/UX Design Intern', 'Internship', 'Design responsive interfaces using Figma and CSS.', 'Delhi', 'Remote', 10000, 0, 'Any Graduate', '0-1 years', date(2026, 11, 22), 'https://example.com/apply/pixelforge-uiux', ['HTML', 'CSS', 'Bootstrap']),
    (4, 'Web Developer (Part-time)', 'Part-time', 'Maintain and update client websites using HTML/CSS/JS.', 'Delhi', 'Remote', 8000, 0, 'Any Graduate', '0-1 years', date(2026, 11, 18), 'https://example.com/apply/pixelforge-webdev', ['HTML', 'CSS', 'JavaScript']),
    (5, 'Cybersecurity Intern', 'Internship', 'Assist with vulnerability assessments and security audits.', 'Bangalore', 'On-site', 18000, 0, 'B.Tech/BCA', '0-1 years', date(2026, 12, 20), 'https://example.com/apply/securenet-cyber', ['Cybersecurity Basics', 'Linux', 'Python']),
    (5, 'Security Analyst (Entry Level)', 'Full-time Job', 'Monitor systems for security threats and incidents.', 'Bangalore', 'Hybrid', 0, 420000, 'B.Tech/BCA', '0-1 years', date(2026, 12, 18), 'https://example.com/apply/securenet-analyst', ['Cybersecurity Basics', 'Linux', 'Python']),
    (6, 'Software Engineer Apprentice', 'Apprenticeship', 'Structured apprenticeship program covering full stack development.', 'Chennai', 'On-site', 16000, 0, 'Any Graduate', '0-1 years', date(2026, 11, 27), 'https://example.com/apply/greenleaf-apprentice', ['Python', 'SQL', 'HTML', 'CSS', 'JavaScript']),
    (6, 'Python Developer Intern', 'Internship', 'Build backend services and automation scripts.', 'Chennai', 'Remote', 15000, 0, 'B.Tech/BCA', '0-1 years', date(2026, 12, 8), 'https://example.com/apply/greenleaf-python', ['Python', 'Git', 'MySQL']),
    (7, 'E-commerce Backend Intern', 'Internship', 'Work on order management APIs with Node.js.', 'Noida', 'Hybrid', 14000, 0, 'B.Tech/BCA', '0-1 years', date(2026, 11, 24), 'https://example.com/apply/orbit-backend', ['Node.js', 'JavaScript', 'REST APIs']),
    (7, 'Junior Software Developer', 'Full-time Job', 'Develop and maintain internal tools using React and Flask.', 'Noida', 'On-site', 0, 400000, 'B.Tech/BCA', '0-2 years', date(2026, 12, 2), 'https://example.com/apply/orbit-junior-dev', ['JavaScript', 'React', 'Flask', 'MySQL']),
    (8, 'Database Intern', 'Internship', 'Design and optimize MySQL databases for internal apps.', 'Kolkata', 'On-site', 12000, 0, 'B.Tech/BCA', '0-1 years', date(2026, 11, 29), 'https://example.com/apply/quantumbyte-db', ['SQL', 'MySQL', 'Excel']),
    (8, 'Software Development Intern', 'Internship', 'General SDE internship covering full stack tasks.', 'Kolkata', 'Remote', 15000, 0, 'B.Tech/BCA', '0-1 years', date(2026, 12, 12), 'https://example.com/apply/quantumbyte-sde', ['Python', 'SQL', 'JavaScript']),
    (9, 'Associate Software Engineer', 'Full-time Job', 'Entry level role building products with React and Node.js.', 'Remote', 'Remote', 0, 450000, 'B.Tech/BCA/MCA', '0-1 years', date(2026, 12, 22), 'https://example.com/apply/skyline-associate', ['JavaScript', 'React', 'Node.js', 'REST APIs']),
    (9, 'Technical Support Intern', 'Internship', 'Provide first-line technical support and bug triage.', 'Remote', 'Remote', 10000, 0, 'Any Graduate', '0-1 years', date(2026, 11, 19), 'https://example.com/apply/skyline-support', ['HTML', 'CSS', 'Git']),
]


def run():
    with app.app_context():
        db.create_all()
        print('Tables created.')

        if Skill.query.count() == 0:
            for name in SKILLS:
                db.session.add(Skill(skill_name=name))
            db.session.commit()
            print(f'{len(SKILLS)} skills seeded.')

        skill_lookup = {s.skill_name: s for s in Skill.query.all()}

        if Company.query.count() == 0:
            company_objs = []
            for name, website in COMPANIES:
                c = Company(company_name=name, website=website, is_verified=False)
                db.session.add(c)
                company_objs.append(c)
            db.session.commit()
            print(f'{len(COMPANIES)} companies seeded (SAMPLE DATA).')
        else:
            company_objs = Company.query.order_by(Company.id).all()

        if Opportunity.query.count() == 0:
            for (c_idx, title, otype, desc, location, work_mode, stipend, salary,
                 edu, exp, deadline, apply_url, skill_names) in OPPORTUNITIES:
                opp = Opportunity(
                    company_id=company_objs[c_idx].id,
                    title=title, type=otype, description=desc, location=location,
                    work_mode=work_mode, stipend=stipend, salary=salary,
                    education_requirement=edu, experience_requirement=exp,
                    deadline=deadline, apply_url=apply_url, is_sample=True,
                )
                opp.skills = [skill_lookup[s] for s in skill_names if s in skill_lookup]
                db.session.add(opp)
            db.session.commit()
            print(f'{len(OPPORTUNITIES)} sample opportunities seeded.')

        if not User.query.filter_by(email='admin@skillmatch.com').first():
            admin = User(name='Admin User', email='admin@skillmatch.com', role='admin')
            admin.set_password('Admin@123')
            db.session.add(admin)
            db.session.commit()
            print('Demo admin created -> email: admin@skillmatch.com | password: Admin@123')

        if not User.query.filter_by(email='student@skillmatch.com').first():
            demo = User(name='Demo Student', email='student@skillmatch.com', role='student')
            demo.set_password('Student@123')
            db.session.add(demo)
            db.session.flush()
            demo_profile = StudentProfile(
                user_id=demo.id, college='Sandip University', course='BCA',
                graduation_year=2027, location='Nashik', looking_for='Both',
                preferred_location='Bangalore', work_mode='Remote',
            )
            demo_profile.skills = [skill_lookup[s] for s in ['Python', 'SQL', 'HTML', 'CSS', 'JavaScript'] if s in skill_lookup]
            db.session.add(demo_profile)
            db.session.commit()
            print('Demo student created -> email: student@skillmatch.com | password: Student@123')

        print('\nDatabase initialization complete.')


if __name__ == '__main__':
    run()
