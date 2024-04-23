from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/frontpage', methods=['GET'])
def frontpage():
    return render_template("front_page.html", user=current_user)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if current_user.role != 'manager':
            flash('You are not authorized to perform this action', category='error')
            return redirect(url_for('views.home'))

        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note and note.user_id == current_user.id:
        if current_user.role != 'manager':
            return jsonify({'error': 'Unauthorized'}), 403
        db.session.delete(note)
        db.session.commit()
    return jsonify({})

@views.route('/get-employees', methods=['GET'])
@login_required
def get_employees():
    if current_user.role != 'manager':
        return jsonify({'error': 'Unauthorized'}), 403

    employees = User.query.filter_by(role='employee').all()  # Adjust query as needed
    employee_data = [{'id': e.id, 'first_name': e.first_name} for e in employees]
    return jsonify(employee_data)

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name')
        current_user.days = ','.join(request.form.getlist('days[]'))
        current_user.times = request.form.get('times')
        current_user.skills = request.form.get('skills')
        db.session.commit()
        flash('Profile updated successfully!', category='success')
    return render_template("profile.html", user=current_user)