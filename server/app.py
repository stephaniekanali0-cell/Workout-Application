from datetime import datetime

from flask import Flask, jsonify, request
from flask_migrate import Migrate
from server.extensions import db, ma
from server.models import Exercise, Workout, WorkoutExercises

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

# import models so Flask-Migrate can detect table metadata
from server import models

# initialize Flask-Migrate with the app and database
migrate = Migrate(app, db)


@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify([
        {
            'id': workout.id,
            'date': workout.date.isoformat(),
            'duration_minutes': workout.duration_minutes,
            'notes': workout.notes,
        }
        for workout in workouts
    ])


@app.route('/workouts/<int:workout_id>', methods=['GET'])
def get_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    return jsonify(
        {
            'id': workout.id,
            'date': workout.date.isoformat(),
            'duration_minutes': workout.duration_minutes,
            'notes': workout.notes,
            'exercises': [
                {
                    'id': assoc.exercise.id,
                    'name': assoc.exercise.name,
                    'category': assoc.exercise.category,
                    'equipment_needed': assoc.exercise.equipment_needed,
                    'reps': assoc.reps,
                    'sets': assoc.sets,
                    'duration_seconds': assoc.duration_seconds,
                }
                for assoc in workout.workout_exercises
            ],
        }
    )


@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json() or {}
    try:
        date_value = datetime.fromisoformat(data['date']).date()
    except (KeyError, ValueError):
        return jsonify({'error': 'date is required and must be YYYY-MM-DD'}), 400

    duration_minutes = data.get('duration_minutes')
    notes = data.get('notes')

    if duration_minutes is None or notes is None:
        return jsonify({'error': 'duration_minutes and notes are required'}), 400

    workout = Workout(date=date_value, duration_minutes=duration_minutes, notes=notes)
    db.session.add(workout)
    db.session.commit()

    return (
        jsonify(
            {
                'id': workout.id,
                'date': workout.date.isoformat(),
                'duration_minutes': workout.duration_minutes,
                'notes': workout.notes,
            }
        ),
        201,
    )


@app.route('/workouts/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    return jsonify({'message': 'Workout deleted'})


@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify([
        {
            'id': exercise.id,
            'name': exercise.name,
            'category': exercise.category,
            'equipment_needed': exercise.equipment_needed,
        }
        for exercise in exercises
    ])


@app.route('/exercises/<int:exercise_id>', methods=['GET'])
def get_exercise(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    return jsonify(
        {
            'id': exercise.id,
            'name': exercise.name,
            'category': exercise.category,
            'equipment_needed': exercise.equipment_needed,
            'workouts': [
                {
                    'id': assoc.workout.id,
                    'date': assoc.workout.date.isoformat(),
                    'duration_minutes': assoc.workout.duration_minutes,
                    'notes': assoc.workout.notes,
                    'reps': assoc.reps,
                    'sets': assoc.sets,
                    'duration_seconds': assoc.duration_seconds,
                }
                for assoc in exercise.workout_exercises
            ],
        }
    )


@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json() or {}
    name = data.get('name')
    category = data.get('category')
    equipment_needed = data.get('equipment_needed')

    if not name or category is None or equipment_needed is None:
        return jsonify({'error': 'name, category, and equipment_needed are required'}), 400

    exercise = Exercise(name=name, category=category, equipment_needed=equipment_needed)
    db.session.add(exercise)
    db.session.commit()

    return (
        jsonify(
            {
                'id': exercise.id,
                'name': exercise.name,
                'category': exercise.category,
                'equipment_needed': exercise.equipment_needed,
            }
        ),
        201,
    )


@app.route('/exercises/<int:exercise_id>', methods=['DELETE'])
def delete_exercise(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({'message': 'Exercise deleted'})


@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get_or_404(workout_id)
    exercise = Exercise.query.get_or_404(exercise_id)
    data = request.get_json() or {}

    workout_exercise = WorkoutExercises(
        workout_id=workout.id,
        exercise_id=exercise.id,
        reps=data.get('reps'),
        sets=data.get('sets'),
        duration_seconds=data.get('duration_seconds'),
    )
    db.session.add(workout_exercise)
    db.session.commit()

    return (
        jsonify(
            {
                'id': workout_exercise.id,
                'workout_id': workout_exercise.workout_id,
                'exercise_id': workout_exercise.exercise_id,
                'reps': workout_exercise.reps,
                'sets': workout_exercise.sets,
                'duration_seconds': workout_exercise.duration_seconds,
            }
        ),
        201,
    )


if __name__ == '__main__':
    app.run(port=5555, debug=True)
