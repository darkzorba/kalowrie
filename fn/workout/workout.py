import datetime

from django.utils import timezone
from fn.base.decorator import Response
from fn.base.exception import ValidationError
from fn.base.sql import SQLQuery
from fn.workout import exercise
from collections import defaultdict

class Workout(SQLQuery):
    def __init__(self, user_id, workout_id = None):
        super().__init__()
        self.user_id = user_id
        self.workout_id = workout_id

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
    def save_workout(self, exercises_list, week_day, name):
        exercises_save_list = []
        existing_exercise_id = set(self.select(f"""
        select we.id
        from public.workout w
        join public.workout_exercise we on we.workout_id = w.id 
                              and we.status = true 
        where w.user_id = :user_id
              and w.id = :workout_id
              and w.status = true
        """, parameters=dict(workout_id=self.workout_id, user_id=self.user_id), is_values_list=True))

        if len(existing_exercise_id) == 0:
            raise ValidationError('No existing workout found.')

        workout_id = self.save('workout', {
            'name': name,
            'week_day': week_day,
            'id': self.workout_id,
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
    def disable_workout(self):
        self.disable('workout', dict_filter={'id':self.workout_id})
        result = self.disable('workout_exercise', dict_filter={'workout_id':self.workout_id})

        if not result:
            raise Exception()


    @Response(desc_error='Error trying to manage session.', return_list=['session_id'])
    def manage_session(self, session_id = None, total_kgs = None, exercises_list = None, is_finished = False):
        if not session_id:
            session_id = self.insert('workout_session', {
            'workout_id': self.workout_id,
            'started_datm':timezone.now()
            })

        if session_id and is_finished:
            dict_session = self.select(f"""
            select s.id,
                   s.started_datm
            from public.workout_session s
            where s.id = :session_id 
                  and s.workout_id = :workout_id  
            """, parameters=dict(workout_id=self.workout_id, session_id=session_id), is_first=True)
            if not dict_session:
                raise ValidationError("No session found.")

            dict_session['finished_datm'] = timezone.now()
            dict_session['total_kgs'] = total_kgs
            dict_session['duration'] = dict_session['finished_datm'] - dict_session['started_datm']
            dict_session['workout_date'] = timezone.now().date()

            session_id = self.save('workout_session', dict_session)

            if exercises_list:
                exercises_insert_list = [
                    {
                        'exercise_id': exercise['id'],
                        'total_kgs': exercise['total_kgs'],
                        'workout_session_id': session_id
                    }
                    for exercise in exercises_list
                ]

                exercises_ids_list = self.bulk_insert('workout_session_exercise', exercises_insert_list)

                sets_insert_list = [
                    {
                        'set_number': exercise_set['set_number'],
                        'reps_done': exercise_set['reps'],
                        'weight': exercise_set['weight'],
                        'reps_in_reserve': exercise_set['rir'],
                        'rest_time': timezone.timedelta(seconds=exercise_set['rest_time']),
                        'session_exercise_id': exercise_id
                    }
                        for exercise, exercise_id in zip(exercises_list, exercises_ids_list)
                        for exercise_set in exercise['sets']
                ]

                sets_ids_list = self.bulk_insert('workout_session_exerciseset', sets_insert_list)

        return session_id

    @Response(desc_error="Error trying to get previous session.", return_list=['previous_session_list'])
    def get_previous_session(self):
        previous_session_id = self.get_previous_session_id()
        exercises_list = self.select(f"""
        select se.exercise_id, 
               ses.set_number,
               ses.reps_done,
               ses.reps_in_reserve,
               ses.weight
        from public.workout_session s
        join join public.workout_session_exercise se
            on se.workout_session_id = s.id
        join join public.workout_session_exerciseset ses 
            on ses.session_exercise_id = se.id 
        where s.id = :previous_session_id
              and s.workout_id = :workout_id 
              and ses.status = true 
              and se.status = true 
              and s.status = true
        order by se.exercise_id, s.id DESC 
        """, parameters=dict(workout_id=self.workout_id, previous_session_id=previous_session_id))

        grouped = defaultdict(list)

        for row in exercises_list:
            grouped[row["exercise_id"]].append({
                "set_number": row["set_number"],
                "reps_done": row["reps_done"],
                "reps_in_reserve": row["reps_in_reserve"],
                "weight": row["weight"],
            })

        exercise_session_list = [
        {"exercise_id": exercise_id, "sets": sets}
        for exercise_id, sets in grouped.items()
        ]

        return exercise_session_list


    @Response(desc_error="Error fetching evolution.", return_list=['evolution_list'])
    def get_workout_exercise_evolution(self, dat_start, dat_end):
        query = """
                select se.exercise_id,
                       ses.weight::float,
                       ses.reps_done::float,
                       ses.reps_in_reserve::float,
                       ses.set_number,
                       se.total_kgs::float, 
                       e.name as exercise_name,
                       ws.workout_date
                from public.workout_session ws
                         join public.workout_session_exercise se
                              on se.workout_session_id = ws.id
                         join public.workout_session_exerciseset ses
                              on ses.session_exercise_id = se.id
                         join public.exercise e
                              on e.id = se.exercise_id
                where se.status = true
                  and ses.status = true
                  and ws.status = true
                  and e.status = true
                  and ws.workout_id = :workout_id
                  and ws.workout_date between :dat_start and :dat_end
                order by se.exercise_id, ws.workout_date, ses.set_number 
                """
        parameters = dict(workout_id=self.workout_id, dat_start=dat_start, dat_end=dat_end)
        evolution_list = self.select(query, parameters=parameters)

        if not evolution_list:
            return []

        grouped_by_exercise = defaultdict(dict)

        for row in evolution_list:
            exercise_id = row['exercise_id']
            date_str = row['workout_date'].isoformat()

            if date_str not in grouped_by_exercise[exercise_id]:
                grouped_by_exercise[exercise_id][date_str] = {
                    'sets': [],
                    'total_kgs': row['total_kgs']
                }

            grouped_by_exercise[exercise_id][date_str]['sets'].append({
                'set_number': row['set_number'],
                'weight': row['weight'],
                'reps_done': row['reps_done'],
                'reps_in_reserve': row['reps_in_reserve']
            })

        final_evolution = []
        for exercise_id, sessions in grouped_by_exercise.items():
            exercise_data = {
                'exercise_id': exercise_id,
                'sessions': []
            }

            for date, session_data in sessions.items():
                sets = session_data['sets']

                max_e1rm = 0
                for s in sets:
                    e1rm = s['weight'] * (1 + s['reps_done'] / 30)
                    if e1rm > max_e1rm:
                        max_e1rm = e1rm

                exercise_data['sessions'].append({
                    'date': date,
                    'sets': sets,
                    'metrics': {
                        'total_volume': session_data['total_kgs'],
                        'max_e1rm': round(max_e1rm, 2)
                    }
                })

            final_evolution.append(exercise_data)

        return final_evolution

    def get_previous_session_id(self):
        return self.select(query=f"""
        select s.id from public.workout_session s 
        join public.workout_session_exercise se
            on se.workout_session_id = s.id 
        where workout_id = :workout_id 
        order by id desc limit 1
        """, parameters={'workout_id': self.workout_id}, is_values_list=True, is_first=True)


    @Response(desc_error="Error fetching last workouts.", return_list=['last_workouts_list'])
    def get_last_workouts(self, days):
        actual_date = datetime.date.today()
        start_date = actual_date - datetime.timedelta(days=days)

        query = f"""
        select se.exercise_id,
               e.image_url as exercise_image,
               e.name as exercise_name, 
               ses.set_number,
               ses.reps_done::float,
               ses.reps_in_reserve::float,
               ses.weight::float,
               s.workout_date,
               w.name as workout_name,
               s.id as session_id,
               s.duration as workout_duration
        from public.workout_session s
        join public.workout w 
            on s.workout_id = w.id
        join public.workout_session_exercise se
            on se.workout_session_id = s.id
        join public.workout_session_exerciseset ses 
            on ses.session_exercise_id = se.id 
        join public.exercise e
            on e.id = se.exercise_id
        where s.workout_date between :dat_start and :dat_end
              and ses.status = true 
              and se.status = true 
              and s.status = true
              and e.status = true
        order by se.exercise_id, s.id DESC 
        """

        exercises_list = self.select(query, parameters=dict(dat_start=start_date,dat_end=actual_date))

        sessions = {}

        for row in exercises_list:
            session = sessions.setdefault(row["session_id"], {
                "workout_name": row["workout_name"],
                "workout_date": row["workout_date"],
                "workout_duration": row["workout_duration"],
                "exercises": {}
            })

            exercise = session["exercises"].setdefault(row["exercise_id"], {
                "exercise_image": row["exercise_image"],
                "exercise_name": row["exercise_name"],
                "sets": []
            })

            exercise["sets"].append({
                "set_number": row["set_number"],
                "reps_done": row["reps_done"],
                "rir": row["reps_in_reserve"],
                "weight": row["weight"]
            })

        last_workouts_list = [
            {
                "workout_name": session_data["workout_name"],
                "workout_date": session_data["workout_date"],
                "exercises": list(session_data["exercises"].values())
            }
            for session_data in sessions.values()
        ]

        return last_workouts_list