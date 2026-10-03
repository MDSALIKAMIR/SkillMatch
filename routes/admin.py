from functools import wraps
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from models import db, User, StudentProfile, Company, Opportunity, Skill, Application

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return wrapper


@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    stats = {
        'total_students': User.query.filter_by(role='student').count(),
        'total_opportunities': Opportunity.query.count(),
        'total_applications': Application.query.count(),
        'total_companies': Company.query.count(),
    }
    recent_opportunities = Opportunity.query.order_by(Opportunity.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html', stats=stats, recent_opportunities=recent_opportunities)


# ==========================
# OPPORTUNITIES CRUD
# ==========================
@admin_bp.route('/opportunities')
@login_required
@admin_required
def opportunities():
    opps = Opportunity.query.order_by(Opportunity.created_at.desc()).all()
    return render_template('admin/opportunities.html', opportunities=opps)


@admin_bp.route('/opportunities/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_opportunity():
    companies = Company.query.order_by(Company.company_name).all()

    if request.method == 'POST':
        opp = _build_opportunity_from_form(Opportunity())
        db.session.add(opp)
        db.session.commit()
        flash('Opportunity created.', 'success')
        return redirect(url_for('admin.opportunities'))

    return render_template('admin/opportunity_form.html', companies=companies, opp=None)


@admin_bp.route('/opportunities/<int:opp_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_opportunity(opp_id):
    opp = Opportunity.query.get_or_404(opp_id)

    if request.method == 'POST':
        _build_opportunity_from_form(opp)
        db.session.commit()

        flash('Opportunity updated.', 'success')
        return redirect(url_for('admin.opportunities'))

    return render_template('admin/opportunity_form.html', opp=opp)

@admin_bp.route('/opportunities/<int:opp_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_opportunity(opp_id):
    opp = Opportunity.query.get_or_404(opp_id)
    db.session.delete(opp)
    db.session.commit()
    flash('Opportunity deleted.', 'success')
    return redirect(url_for('admin.opportunities'))


def _build_opportunity_from_form(opp):
    
    # Company name entered manually
    company_name = request.form.get('company_name', '').strip()

    if not company_name:
        raise ValueError('Company name is required.')

    # Check existing company (case-insensitive)
    company = Company.query.filter(
        db.func.lower(Company.company_name) == company_name.lower()
    ).first()

    # Create company automatically if it doesn't exist
    if not company:
        company = Company(
            company_name=company_name,
            website='',
            is_verified=False
        )
        db.session.add(company)
        db.session.flush()

    opp.company_id = company.id

    opp.title = request.form.get('title', '').strip()
    opp.type = request.form.get('type')
    opp.description = request.form.get('description', '').strip()
    opp.location = request.form.get('location', '').strip()
    opp.work_mode = request.form.get('work_mode')

    stipend = request.form.get('stipend', '0').strip()
    opp.stipend = int(stipend) if stipend.isdigit() else 0

    salary = request.form.get('salary', '0').strip()
    opp.salary = int(salary) if salary.isdigit() else 0

    opp.education_requirement = request.form.get(
        'education_requirement', ''
    ).strip()

    opp.experience_requirement = request.form.get(
        'experience_requirement', ''
    ).strip()

    deadline = request.form.get('deadline', '').strip()
    opp.deadline = (
        datetime.strptime(deadline, '%Y-%m-%d').date()
        if deadline else None
    )

    opp.apply_url = request.form.get('apply_url', '').strip()
    opp.is_sample = bool(request.form.get('is_sample'))

    skills_raw = request.form.get('required_skills', '')

    skill_names = [
        s.strip()
        for s in skills_raw.split(',')
        if s.strip()
    ]

    opp.skills = []

    for name in skill_names:
        skill = Skill.query.filter(
            db.func.lower(Skill.skill_name) == name.lower()
        ).first()

        if not skill:
            skill = Skill(skill_name=name)
            db.session.add(skill)
            db.session.flush()

        opp.skills.append(skill)

    return opp


# ==========================
# COMPANIES
# ==========================
@admin_bp.route('/companies', methods=['GET', 'POST'])
@login_required
@admin_required
def companies():
    if request.method == 'POST':
        name = request.form.get('company_name', '').strip()
        if name:
            db.session.add(Company(
                company_name=name,
                website=request.form.get('website', '').strip(),
                is_verified=bool(request.form.get('is_verified'))
            ))
            db.session.commit()
            flash('Company added.', 'success')
        return redirect(url_for('admin.companies'))

    all_companies = Company.query.order_by(Company.company_name).all()
    return render_template('admin/companies.html', companies=all_companies)


@admin_bp.route('/companies/<int:company_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_company(company_id):
    company = Company.query.get_or_404(company_id)
    db.session.delete(company)
    db.session.commit()
    flash('Company deleted.', 'success')
    return redirect(url_for('admin.companies'))


# ==========================
# STUDENTS
# ==========================
@admin_bp.route('/students')
@login_required
@admin_required
def students():
    all_students = User.query.filter_by(role='student').order_by(User.created_at.desc()).all()
    return render_template('admin/students.html', students=all_students)


# ==========================
# APPLICATIONS (view only)
# ==========================
@admin_bp.route('/applications')
@login_required
@admin_required
def applications():
    apps = Application.query.order_by(Application.updated_at.desc()).all()
    return render_template('admin/applications.html', apps=apps)


# ==========================
# SKILLS
# ==========================
@admin_bp.route('/skills', methods=['GET', 'POST'])
@login_required
@admin_required
def skills():
    if request.method == 'POST':
        name = request.form.get('skill_name', '').strip()
        if name and not Skill.query.filter(db.func.lower(Skill.skill_name) == name.lower()).first():
            db.session.add(Skill(skill_name=name))
            db.session.commit()
            flash('Skill added.', 'success')
        return redirect(url_for('admin.skills'))

    all_skills = Skill.query.order_by(Skill.skill_name).all()
    return render_template('admin/skills.html', skills=all_skills)


@admin_bp.route('/skills/<int:skill_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    flash('Skill deleted.', 'success')
    return redirect(url_for('admin.skills'))
