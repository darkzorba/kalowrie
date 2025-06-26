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
    def save_exercise(self, name, type_id, muscle_group_id, equipment_id, image = None, team_id = None, video = None):
        if image:
            image = Files().upload_file(file=image, storage_folder='exercises', file_type='image')
        dict_exercise = {
            'name': name,
            'exercise_type_id': type_id,
            'muscle_group_id': muscle_group_id,
            'equipment_id': equipment_id,
            'image_url': image,
            'team_id': team_id,
        }

        exercise_id = self.save('public.exercise', dict_exercise)

        return exercise_id


    @Response(desc_error="Error fetching muscular groups.", return_list=['muscular_groups'])
    def get_muscular_groups(self):
        return self.select(f"""
        select mg.id,
               mg.name 
        from public.muscle_group mg 
        where mg.status = true
        """)

    @Response(desc_error="Error fetching exercise types.", return_list=['exercise_types'])
    def get_exercise_types(self):
        return self.select(f"""
            select et.id,
                   et.name 
            from public.exercise_type et 
            where et.status = true
            """)

    @Response(desc_error="Error fetching exercise equipments.", return_list=['exercise_equipments'])
    def get_exercise_equipments(self):
        return self.select(f"""
            select ee.id,
                   ee.name 
            from public.exercise_equipment ee 
            where ee.status = true
            """)