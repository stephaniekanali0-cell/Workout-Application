from .extensions import db
from sqlalchemy.orm import validates

# Models defined
class Exercise(db.Model):
    __tablename__ = "exercises"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)
    workout_exercises = db.relationship(
        "WorkoutExercises",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )
    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        back_populates="exercises"
    )

class Workout(db.Model):
    __tablename__ = "workouts"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String(100), nullable=False)
    workout_exercises = db.relationship(
        "WorkoutExercises",
        back_populates="workout",
        cascade="all, delete-orphan"
    )
    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        back_populates="workouts"
    )

class WorkoutExercises(db.Model):
    __tablename__ = "workout_exercises"
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)
    exercise = db.relationship("Exercise", back_populates="workout_exercises")
    workout = db.relationship("Workout", back_populates="workout_exercises")