from application import app
from application import db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user,logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from datetime import datetime
import pytz
from .models import User, Exerciselist, Workout, Exercise, Set

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/workout_log')
@login_required
def workout_log():
    workouts = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.date.desc()).all()
    return render_template('workout_log.html', workouts=workouts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login Successful!", category="success")
            return redirect(url_for('workout_log'))
        else:
            flash("Invalid username or password! Please try again.", category="danger")
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        unhashed_password = request.form['password']

        user_username = User.query.filter_by(username=username).first()

        if user_username:
            flash("Username already exists!", category="danger")
            return redirect(url_for('register'))

        user = User(
            firstname=firstname,
            lastname=lastname,
            username=username, 
            unhashed_password=unhashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash("Registration Successful!", category="success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/add_workout', methods=['POST', 'GET'])
@login_required
def add_workout():
    if request.method == 'POST':
        user = User.query.filter_by(username = current_user.username).first()
        workout = Workout(date=datetime.now(), user_id=user.id)
        exercise_count = int(request.form['exercise_count'])

        for exercise_num in range(1,exercise_count + 1):
            exercise = Exercise(order=exercise_num, exercise_id=request.form['exercise'+str(exercise_num)], workout=workout)
            weights = request.form.getlist('weight' + str(exercise_num))
            reps = request.form.getlist('reps' + str(exercise_num))
            set_order = 1
            for weight, rep in zip(weights, reps):
                work_set = Set(order=set_order, exercise=exercise, weight=weight, reps=rep)
                set_order += 1

        db.session.add(workout)
        db.session.commit()
        flash("Workout Added!", category="success")
        return redirect(url_for('workout_log'))

    exercises = Exerciselist.query.all()
    return render_template('add_workout.html', exercises=exercises)

@app.route('/edit', methods=['POST','GET'])
@login_required
def edit():
    if request.method == 'POST':
        workout_id = int(request.form['workout_id'])
        workout = Workout.query.filter_by(id = workout_id).first()
        for exercise in workout.exercises:
            for set in exercise.sets:
                set.weight = request.form['weight' + str(set.id)]
                set.reps = request.form['reps' + str(set.id)]
        db.session.commit()
        flash("Workout updated!", category="success")
        return redirect(url_for('workout_log'))

@app.route('/delete', methods=['POST','GET'])
@login_required
def delete():
    if request.method == 'POST':
        workout_id = int(request.form['workout_id'])
        workout = Workout.query.filter_by(id = workout_id).first()
        db.session.delete(workout)
        db.session.commit()
        flash("Workout deleted!", category="warning")
        return redirect(url_for('workout_log'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", category="warning")
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'),500