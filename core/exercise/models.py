from django.db import models

import core.models


# Create your models here.




class Exercise(core.models.Log):
    name = models.CharField(max_length=200)
    exercise_type = models.ForeignKey('exercise.ExerciseType', on_delete=models.DO_NOTHING, null=True)
    muscle_group = models.ForeignKey('exercise.MuscleGroup', on_delete=models.DO_NOTHING, null=True)
    equipment = models.ForeignKey('exercise.ExerciseEquipment', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = '"public"."exercise"'




class ExerciseType(core.models.Log):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = '"public"."exercise_type"'


class ExerciseEquipment(core.models.Log):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = '"public"."exercise_equipment"'


class MuscleGroup(core.models.Log):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = '"public"."muscle_group"'