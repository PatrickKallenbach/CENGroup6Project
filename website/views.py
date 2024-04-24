from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Note, Shift
from . import db
import json
from sqlalchemy import exists

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

    # Query shifts for the current user
    shifts = Shift.query.filter_by(user_id=current_user.id).all()
    shifts_data = [{
        'month': shift.month,
        'day': shift.day,
        'type': shift.type
    } for shift in shifts]

    return render_template("home.html", user=current_user, shifts=shifts_data)


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

    employees = User.query.filter_by(role='employee').all()  
    employee_data = [{'id': e.id, 'first_name': e.first_name} for e in employees]
    return jsonify(employee_data)

@views.route('/create_shift', methods=['POST'])
def create_shift():
    data = request.get_json()
    user = User.query.filter_by(id=data['user_id']).first()
    if db.session.query(exists()
                        .where(Shift.user == user)
                        .where(Shift.month == data['month'])
                        .where(Shift.day == data['day'])
                        .where(Shift.type == data['type'])
                        ).scalar():
        return jsonify({'error': 'Shift already exists!'})
    else:
        new_shift = Shift(user=user, month=data['month'], day=data['day'], type=data['type'])
        db.session.add(new_shift)
        db.session.commit()
        return jsonify({'message': 'Shift created!'})

@views.route('/delete_shift', methods=['DELETE'])
def delete_shift():
    data = request.get_json()
    id = data['id']
    shift = Shift.query.get(id)
    if shift:
        db.session.delete(shift)
        db.session.commit()
        return jsonify({'message': 'Shift deleted!'})
    else:
        return jsonify({'message': 'Shift not found!'})
    
@views.route('/get_shifts', methods=['GET'])
@login_required
def get_shifts():
    # if current_user.role == 'employee':
    #     # Fetch only shifts for the logged-in employee
    #     shifts = Shift.query.filter_by(user_id=current_user.id).all()
    # else:
    #     # Alternatively, for managers or other roles, you might want to return different data
    #     # or handle it accordingly
    #     return jsonify({'error': 'Unauthorized'}), 403

    
    shifts = Shift.query.all()

    shifts_list = [{
        'id': shift.id,
        'first_name': shift.user.first_name,
        'month': shift.month,
        'day': shift.day,
        'type': shift.type
    } for shift in shifts]

    return jsonify(shifts_list)


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
