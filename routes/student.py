import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, StudentProfile, Skill, Project, Opportunity, SavedOpportunity, Application
from services.matching import calculate_match, rank_opportunities, resume_skill_suggestions

student_bp = Blueprint('student', __name__)


def get_profile():
    return current_user.profile


def allowed_resume(filename):
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    return ext in current_app.config['ALLOWED_RESUME_EXTENSIONS']


# ==========================
# DASHBOARD
# ==========================
@student_bp.route('/dashboard')
@login_required
def dashboard():
    profile = get_profile()
    opportunities = Opportunity.query.all()
    ranked = rank_opportunities(profile, opportunities)[:6]  # top 6 recommended

    stats = {
        'saved': len(profile.saved),
        'applied': Application.query.filter_by(student_id=profile.id).count(),
        'shortlisted': Application.query.filter_by(student_id=profile.id, status='Shortlisted').count(),
        'selected': Application.query.filter_by(student_id=profile.id, status='Selected').count(),
    }

    return render_template('dashboard.html', ranked=ranked, profile=profile, stats=stats)


# ==========================
# PROFILE
# ==========================
@student_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile = get_profile()

    if request.method == 'POST':
        profile.college = request.form.get('college', '').strip()
        profile.course = request.form.get('course', '').strip()
        grad_year = request.form.get('graduation_year', '').strip()
        profile.graduation_year = int(grad_year) if grad_year.isdigit() else None
        cgpa = request.form.get('cgpa', '').strip()
        profile.cgpa = float(cgpa) if cgpa else None
        profile.location = request.form.get('location', '').strip()

        profile.looking_for = request.form.get('looking_for', 'Both')
        stipend = request.form.get('expected_stipend', '0').strip()
        profile.expected_stipend = int(stipend) if stipend.isdigit() else 0
        salary = request.form.get('expected_salary', '0').strip()
        profile.expected_salary = int(salary) if salary.isdigit() else 0
        profile.preferred_location = request.form.get('preferred_location', '').strip()
        profile.work_mode = request.form.get('work_mode', 'Any')
        profile.availability = request.form.get('availability', '').strip()

        profile.github = request.form.get('github', '').strip()
        profile.linkedin = request.form.get('linkedin', '').strip()
        profile.portfolio = request.form.get('portfolio', '').strip()

        current_user.name = request.form.get('name', current_user.name).strip()
        current_user.phone = request.form.get('phone', current_user.phone or '').strip()

        # Skills: comma-separated input
        skills_raw = request.form.get('skills', '')
        skill_names = [s.strip() for s in skills_raw.split(',') if s.strip()]
        profile.skills = []
        for name in skill_names:
            skill = Skill.query.filter(db.func.lower(Skill.skill_name) == name.lower()).first()
            if not skill:
                skill = Skill(skill_name=name)
                db.session.add(skill)
                db.session.flush()
            profile.skills.append(skill)

        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('student.profile'))

    return render_template('profile.html', profile=profile)


@student_bp.route('/profile/resume/upload', methods=['POST'])
@login_required
def upload_resume():
    profile = get_profile()
    file = request.files.get('resume')

    if not file or file.filename == '':
        flash('Please choose a PDF file to upload.', 'error')
        return redirect(url_for('student.profile'))

    if not allowed_resume(file.filename):
        flash('Only PDF files are allowed for resumes.', 'error')
        return redirect(url_for('student.profile'))

    os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
    filename = secure_filename(f"resume_user{current_user.id}_{int(datetime.utcnow().timestamp())}.pdf")
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    profile.resume_path = filename
    db.session.commit()
    flash('Resume uploaded successfully.', 'success')
    return redirect(url_for('student.profile'))


@student_bp.route('/profile/resume/download')
@login_required
def download_resume():
    profile = get_profile()
    if not profile.resume_path:
        flash('No resume uploaded yet.', 'error')
        return redirect(url_for('student.profile'))
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], profile.resume_path, as_attachment=True)


@student_bp.route('/profile/resume/analyze')
@login_required
def analyze_resume():
    """Rule-based resume analyzer (no external AI API required)."""
    profile = get_profile()
    student_skills = profile.skill_names()

    # Compare against the union of skills required across all opportunities
    all_required = set()
    for opp in Opportunity.query.all():
        all_required |= opp.required_skill_names()

    matched = sorted(student_skills & all_required)
    missing = sorted(all_required - student_skills)[:8]  # cap suggestions

    suggestions = resume_skill_suggestions(
        matched, missing,
        has_projects=len(profile.projects) > 0,
        has_github=bool(profile.github)
    )

    return render_template('resume_analysis.html', profile=profile, matched=matched,
                            missing=missing, suggestions=suggestions)


# ==========================
# PROJECTS
# ==========================
@student_bp.route('/profile/projects/add', methods=['POST'])
@login_required
def add_project():
    profile = get_profile()
    name = request.form.get('project_name', '').strip()
    if not name:
        flash('Project name is required.', 'error')
        return redirect(url_for('student.profile'))

    project = Project(
        student_id=profile.id,
        project_name=name,
        description=request.form.get('description', '').strip(),
        technologies=request.form.get('technologies', '').strip(),
        github_url=request.form.get('github_url', '').strip(),
        live_url=request.form.get('live_url', '').strip(),
    )
    db.session.add(project)
    db.session.commit()
    flash('Project added.', 'success')
    return redirect(url_for('student.profile'))


@student_bp.route('/profile/projects/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    profile = get_profile()
    project = Project.query.filter_by(id=project_id, student_id=profile.id).first_or_404()
    db.session.delete(project)
    db.session.commit()
    flash('Project removed.', 'success')
    return redirect(url_for('student.profile'))


# ==========================
# OPPORTUNITIES: SEARCH / FILTER / LIST
# ==========================
@student_bp.route('/opportunities')
@login_required
def opportunities():
    profile = get_profile()

    query = Opportunity.query
    q = request.args.get('q', '').strip()
    opp_type = request.args.get('type', '')
    work_mode = request.args.get('work_mode', '')
    location = request.args.get('location', '').strip()
    min_stipend = request.args.get('min_stipend', '')
    max_stipend = request.args.get('max_stipend', '')
    skill_filter = request.args.get('skill', '').strip()
    sort_by = request.args.get('sort', 'match')

    if q:
        from models import Company
        like = f"%{q}%"
        query = query.join(Company).filter(
            db.or_(Opportunity.title.ilike(like), Company.company_name.ilike(like))
        )
    if opp_type:
        query = query.filter(Opportunity.type == opp_type)
    if work_mode:
        query = query.filter(Opportunity.work_mode == work_mode)
    if location:
        query = query.filter(Opportunity.location.ilike(f"%{location}%"))
    if min_stipend.isdigit():
        query = query.filter((Opportunity.stipend >= int(min_stipend)) | (Opportunity.salary >= int(min_stipend)))
    if max_stipend.isdigit():
        query = query.filter((Opportunity.stipend <= int(max_stipend)) | (Opportunity.salary <= int(max_stipend)))
    if skill_filter:
        query = query.join(Opportunity.skills).filter(Skill.skill_name.ilike(f"%{skill_filter}%"))

    results = query.all()
    ranked = rank_opportunities(profile, results)

    if sort_by == 'latest':
        ranked.sort(key=lambda r: r['opportunity'].created_at, reverse=True)
    elif sort_by == 'stipend':
        ranked.sort(key=lambda r: (r['opportunity'].stipend or r['opportunity'].salary or 0), reverse=True)
    elif sort_by == 'deadline':
        ranked.sort(key=lambda r: r['opportunity'].deadline or datetime.max.date())
    # default 'match' keeps rank_opportunities ordering

    all_skills = Skill.query.order_by(Skill.skill_name).all()

    return render_template('opportunities.html', ranked=ranked, filters=request.args,
                            all_skills=all_skills, saved_ids={s.opportunity_id for s in profile.saved})


@student_bp.route('/opportunities/<int:opp_id>')
@login_required
def opportunity_details(opp_id):
    profile = get_profile()
    opp = Opportunity.query.get_or_404(opp_id)
    match = calculate_match(profile.skill_names(), opp.required_skill_names())
    is_saved = SavedOpportunity.query.filter_by(student_id=profile.id, opportunity_id=opp.id).first() is not None
    application = Application.query.filter_by(student_id=profile.id, opportunity_id=opp.id).first()

    return render_template('opportunity_details.html', opp=opp, match=match,
                            is_saved=is_saved, application=application)


# ==========================
# SAVE / UNSAVE
# ==========================
@student_bp.route('/opportunities/<int:opp_id>/save', methods=['POST'])
@login_required
def save_opportunity(opp_id):
    profile = get_profile()
    existing = SavedOpportunity.query.filter_by(student_id=profile.id, opportunity_id=opp_id).first()
    if not existing:
        db.session.add(SavedOpportunity(student_id=profile.id, opportunity_id=opp_id))
        db.session.commit()
        flash('Opportunity saved.', 'success')
    return redirect(request.referrer or url_for('student.opportunities'))


@student_bp.route('/opportunities/<int:opp_id>/unsave', methods=['POST'])
@login_required
def unsave_opportunity(opp_id):
    profile = get_profile()
    existing = SavedOpportunity.query.filter_by(student_id=profile.id, opportunity_id=opp_id).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        flash('Removed from saved opportunities.', 'success')
    return redirect(request.referrer or url_for('student.saved'))


@student_bp.route('/saved')
@login_required
def saved():
    profile = get_profile()
    saved_items = SavedOpportunity.query.filter_by(student_id=profile.id).all()
    results = []
    for item in saved_items:
        match = calculate_match(profile.skill_names(), item.opportunity.required_skill_names())
        results.append({'opportunity': item.opportunity, 'match': match})
    return render_template('saved.html', results=results)


# ==========================
# APPLICATION TRACKER
# ==========================
@student_bp.route('/applications')
@login_required
def applications():
    profile = get_profile()
    apps = Application.query.filter_by(student_id=profile.id).order_by(Application.updated_at.desc()).all()

    stats = {
        'Applied': 0, 'Shortlisted': 0, 'Interview': 0, 'Selected': 0, 'Rejected': 0, 'Saved': 0
    }
    for a in apps:
        stats[a.status] = stats.get(a.status, 0) + 1

    return render_template('applications.html', apps=apps, stats=stats)


@student_bp.route('/opportunities/<int:opp_id>/apply', methods=['POST'])
@login_required
def mark_applied(opp_id):
    profile = get_profile()
    existing = Application.query.filter_by(student_id=profile.id, opportunity_id=opp_id).first()
    if not existing:
        existing = Application(student_id=profile.id, opportunity_id=opp_id, status='Applied',
                                applied_date=datetime.utcnow().date())
        db.session.add(existing)
    else:
        existing.status = 'Applied'
        existing.applied_date = datetime.utcnow().date()
    db.session.commit()
    flash('Marked as applied. Track its progress in My Applications.', 'success')
    return redirect(request.referrer or url_for('student.applications'))


@student_bp.route('/applications/<int:app_id>/update', methods=['POST'])
@login_required
def update_application(app_id):
    profile = get_profile()
    app = Application.query.filter_by(id=app_id, student_id=profile.id).first_or_404()
    app.status = request.form.get('status', app.status)
    app.notes = request.form.get('notes', app.notes)
    db.session.commit()
    flash('Application updated.', 'success')
    return redirect(url_for('student.applications'))


@student_bp.route('/applications/<int:app_id>/delete', methods=['POST'])
@login_required
def delete_application(app_id):
    profile = get_profile()
    app = Application.query.filter_by(id=app_id, student_id=profile.id).first_or_404()
    db.session.delete(app)
    db.session.commit()
    flash('Application removed.', 'success')
    return redirect(url_for('student.applications'))
