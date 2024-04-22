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

@views.route('/create_shift', methods=['POST'])
def create_shift():
    data = request.get_json()
    user = User.query.filter_by(id=data['user_id']).first()
    new_shift = Shift(user=user, month=data['month'], day=data['day'], type=data['type'])
    db.session.add(new_shift)
    db.session.commit()
    return jsonify({'message': 'Shift created!'})

@views.route('/delete_shift/<id>', methods=['DELETE'])
def delete_shift(id):
    shift = Shift.query.get(id)
    if shift:
        db.session.delete(shift)
        db.session.commit()
        return jsonify({'message': 'Shift deleted!'})
    else:
        return jsonify({'message': 'Shift not found!'})
    
@views.route('/get_shifts', methods=['GET'])
def get_shifts():
    shifts = Shift.query.all()
    shifts_list = []
    for shift in shifts:
        shifts_list.append({
            'id': shift.id,
            'user_id': shift.user_id,
            'month': shift.month,
            'day': shift.day,
            'type': shift.type
        })
    return jsonify(shifts_list)

@views.route('/get_user/<first_name>', methods=['GET'])
def get_user(first_name):
    user = User.query.filter_by(first_name=first_name).first()
    user_info = {
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name
    }
    return jsonify(user_info)
'''@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name')
        current_user.days = ','.join(request.form.getlist('days[]'))
        current_user.times = request.form.get('times')
        current_user.skills = request.form.get('skills')
        db.session.commit()
        return jsonify({'message': 'Shift assigned successfully'}), 200
    return jsonify({'error': 'Unauthorized'}), 403

@views.route('/get-shifts', methods=['GET'])
@login_required
def get_shifts():
    date = request.args.get('date')
    shifts = Shift.query.filter_by(date=date).all()
    shift_details = [{'employee_name': shift.employee.first_name, 'shift_id': shift.id} for shift in shifts]
    return jsonify(shift_details), 200
