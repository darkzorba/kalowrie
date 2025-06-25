from fn.base.decorator import Response
from fn.base.sql import SQLQuery
from fn.files.files import Files


class Exercise(SQLQuery):
    def __init__(self):
        super().__init__()

    @Response(desc_error="Error trying to get exercises.", return_list=['exercises_list'])
    def get_all_exercises(self, team_id):
        str_filter = '\n and (e.team_id isnull \n'

        if team_id:
            str_filter += '\n or e.team_id = :team_id)'
        else:
            str_filter += ')'

        return self.select(f"""
        select e.id,
               e.name,
               tp.name as exercise_type,
               mg.name as muscle_group,
               et.name as exercise_equipment,
               e.image_url as exercise_image
        from public.exercise e
            left join public.muscle_group mg on mg.id = e.muscle_group_id
            left join public.exercise_type tp on tp.id = e.exercise_type_id
            left join public.exercise_equipment et on et.id = e.equipment_id
        where e.status = true
              and et.status = true
              and tp.status = true
              and mg.status = true
              {str_filter}  
        """, parameters=dict(team_id=team_id))

    @Response(desc_error="Error trying to save exercise.", return_list=['exercise_id'])
    def save_exercise(self, name, type_id, muscle_group_id, equipment_id, image):
        image_url = Files().upload_file(file=image, storage_folder='exercises', file_type='image')
        dict_exercise = {
            'name': name,
            'type_id': type_id,
            'muscle_group_id': muscle_group_id,
            'equipment_id': equipment_id,
            'image': image_url
        }

        exercise_id = self.save('public.exercise', dict_exercise)

        return exercise_id

