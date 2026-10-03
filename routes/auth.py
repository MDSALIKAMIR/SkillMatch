from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, StudentProfile
from datetime import datetime

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        college = request.form.get('college', '').strip()
        course = request.form.get('course', '').strip()
        graduation_year = request.form.get('graduation_year', '').strip()
        location = request.form.get('location', '').strip()

        errors = []
        if not name or not email or not password:
            errors.append('Name, email and password are required.')
        if len(password) < 6:
            errors.append('Password must be at least 6 characters.')
        if password != confirm:
            errors.append('Passwords do not match.')
        if User.query.filter_by(email=email).first():
            errors.append('An account with this email already exists.')

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('register.html', form_data=request.form)

        user = User(name=name, email=email, phone=phone, role='student')
        user.set_password(password)
        db.session.add(user)
        db.session.flush()  # get user.id before commit

        profile = StudentProfile(
            user_id=user.id,
            college=college,
            course=course,
            graduation_year=int(graduation_year) if graduation_year.isdigit() else None,
            location=location,
        )
        db.session.add(profile)
        db.session.commit()

        login_user(user)
        flash('Welcome to SkillMatch! Complete your profile to get matched.', 'success')
        return redirect(url_for('student.profile'))

    return render_template('register.html', form_data={})


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.name}!', 'success')
            if user.is_admin():
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('student.dashboard'))

        flash('Invalid email or password.', 'error')

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))
