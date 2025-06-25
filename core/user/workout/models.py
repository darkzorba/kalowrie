from django.db import models

import core.models


# Create your models here.




class Workout(core.models.Log):
    name = models.CharField(max_length=200)
    week_day = models.CharField(max_length=200)
    user = models.ForeignKey('user.User', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = u'"public"."workout"'


class WorkoutExercise(core.models.Log):
    workout = models.ForeignKey('workout.Workout', on_delete=models.DO_NOTHING, null=True)
    exercise = models.ForeignKey('exercise.Exercise', on_delete=models.DO_NOTHING, null=True)
    sets = models.IntegerField(null=True)
    min_reps = models.IntegerField(null=True)
    max_reps = models.IntegerField(null=True)
    observations = models.TextField(null=True)
    exercise_order = models.IntegerField(null=True)

    class Meta:
        db_table = u'"public"."workout_exercise"'


class WorkoutSession(core.models.Log):
    workout = models.ForeignKey('workout.Workout', on_delete=models.DO_NOTHING, null=True)
    workout_date = models.DateField(null=True)
    started_datm = models.DateTimeField(null=True)
    finished_datm = models.DateTimeField(null=True)
    duration = models.DurationField(null=True)
    total_kgs = models.DecimalField(max_digits=14, decimal_places=2, null=True)

    class Meta:
        db_table = u'"public"."workout_session"'


class WorkoutSessionExercise(core.models.Log):
    workout_session = models.ForeignKey('workout.WorkoutSession', on_delete=models.DO_NOTHING, null=True)
    exercise = models.ForeignKey('exercise.Exercise', on_delete=models.DO_NOTHING, null=True)
    total_kgs = models.DecimalField(max_digits=14, decimal_places=2, null=True)

    class Meta:
        db_table = u'"public"."workout_session_exercise"'


class WorkoutSessionExerciseSet(core.models.Log):
    session_exercise = models.ForeignKey('workout.WorkoutSessionExercise', on_delete=models.DO_NOTHING, null=True)
    set_number = models.IntegerField(null=True)
    reps_done = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    weight = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    rest_time = models.TimeField(null=True)
    observations = models.TextField(null=True)
    reps_in_reserve = models.IntegerField(null=True)

    class Meta:
        db_table = u'"workout_session_exerciseset"'