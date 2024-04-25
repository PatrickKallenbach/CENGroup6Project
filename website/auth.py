from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import re

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash('You have successfully logged into SwampBites Scheduling!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else:
            flash('Incorrect email or password. Please try again.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.frontpage'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        role = request.form.get('role')
        code = request.form.get('code')

        manager_code = "MANAGER123"
        employee_code = "EMPLOYEE456"

        if (role == "manager" and code != manager_code) or (role == "employee" and code != employee_code):
            flash('Invalid enrollment code for selected role.', category='error')
            return render_template("sign_up.html", user=current_user)

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already in use.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        else:
            # Create and log in the user
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'), role=role)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created.', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
