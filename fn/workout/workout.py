from fn.base.decorator import Response
from fn.base.exception import ValidationError
from fn.base.sql import SQLQuery


class Workout(SQLQuery):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    @Response(desc_error="Error fetching workout", return_list=['workouts_list'])
    def get_user_workout_split(self):
        return self.select("""
        select w.id,
               w.name as workout_name,
               w.week_day,
               json_agg(json_build_object(
                'we_id', we.id,
                'id', we.exercise_id,
               'exercise_name',e.name,
               'exercise_image', e.image_url,
               'sets', we.sets,
               'min_reps', we.min_reps,
               'max_reps', we.max_reps,
               'observations',we.observations
               )) as exercises_list
        from public.workout w
            join public.workout_exercise we on we.workout_id = w.id and we.status = true
            join public.exercise e on we.exercise_id = e.id and e.status = true
        where w.status = true
              and w.user_id = :user_id
        group by w.id, w.name, w.week_day;
        """, parameters=dict(user_id=self.user_id))


    @Response(desc_error="Error saving workout split.", return_list=[])
    def save_workout_split(self, workouts_list):
        workouts_insert_list = [{
                'name': workout['name'],
                'week_day': workout['day_of_week'],
                'user_id': self.user_id,
            } for workout in workouts_list]

        workouts_ids_list = self.bulk_insert('workout', workouts_insert_list)

        exercises_insert_list = [
            {
                'exercise_id': exercise['exercise_id'],
                'min_reps': exercise['min_reps'],
                'max_reps': exercise['max_reps'],
                'observations': exercise['notes'],
                'exercise_order': exercise['order'],
                'sets': exercise['sets'],
                'workout_id': workout_id
            }
            for workout, workout_id in zip(workouts_list, workouts_ids_list)
            for exercise in workout['exercises']
        ]

        self.bulk_insert('workout_exercise', exercises_insert_list)

        return workouts_insert_list

    @Response(desc_error="Error saving workout.", return_list=[])
    def save_workout(self, workout_id, exercises_list, week_day, name):
        exercises_save_list = []
        existing_exercise_id = set(self.select(f"""
        select we.id
        from public.workout w
        join public.workout_exercise we on we.workout_id = w.id 
                              and we.status = true 
        where w.user_id = :user_id
              and w.id = :workout_id
              and w.status = true
        """, parameters=dict(workout_id=workout_id, user_id=self.user_id), is_values_list=True))

        if len(existing_exercise_id) == 0:
            raise ValidationError('No existing workout found.')

        workout_id = self.save('workout', {
            'name': name,
            'week_day': week_day,
            'id': workout_id,
        })

        for exercise in exercises_list:
            workout_exercise_dict = {
                'exercise_id': exercise['exercise_id'],
                'max_reps': exercise['max_reps'],
                'min_reps': exercise['min_reps'],
                'exercise_order': exercise['order'],
                'sets': exercise['sets'],
                'workout_id': workout_id,
                'observations': exercise['notes'],
                'id':exercise['we_id']
            }

            exercises_save_list.append(workout_exercise_dict)

        saved_exercises_ids = set(self.bulk_upsert('workout_exercise', exercises_save_list))

        self.disable('workout_exercise', dict_filter={'id':list(existing_exercise_id - saved_exercises_ids)})



        return workout_id

    @Response(desc_error="Error deleting workout.", return_list=[])
    def disable_workout(self, workout_id):
        self.disable('workout', dict_filter={'id':workout_id})
        result = self.disable('workout_exercise', dict_filter={'workout_id':workout_id})

        if not result:
            raise Exception()
