from fn.base.decorator import Response
from fn.base.sql import SQLQuery
from fn.user.user import User
from core.user.models import User as UserModel
from django.utils import timezone



class Team(SQLQuery):
    def __init__(self, team_id):
        super().__init__()
        self.team_id = team_id


    @Response(desc_error='Error trying to save student.', return_list=['student_id'])
    def save_student(self, height, weight, first_name, last_name, email, gender, age, password, birth_date):
        User.validate_password(password)
        new_user_obj = UserModel(email=email, first_name=first_name, last_name=last_name, username=email, age=age,
                                 gender=gender, height=height, weight=weight,birth_date=birth_date, status=True,
                                 datm_insert=timezone.now(), user_type='student',team_id=self.team_id)
        new_user_obj.set_password(password)
        new_user_obj.save()

        return new_user_obj.id


    @Response(desc_error='Error trying to fetch students.', return_list=['students_list'])
    def get_all_students(self):
        return self.select(f"""
        select u.id,
               concat(u.first_name, ' ', u.last_name) as student_name
        from public.user u 
        where u.status = True 
              and u.user_type = 'student'
              and u.team_id = :team_id
        """, parameters=dict(team_id=self.team_id))


    @Response(desc_error='Error trying to get student infos.', return_list=['student_dict'])
    def get_student(self, student_id):
        return self.select(f"""
        select u.id,
               u.first_name,
               u.last_name,
               u.email,
               u.gender,
               u.height,
               u.weight,
               u.birth_date,
               u.age
        from public.user u 
        where u.status = True
              and u.team_id = :team_id 
              and u.user_type = 'student'
              and u.id = :student_id
        """, parameters=dict(team_id=self.team_id, student_id=student_id), is_first=True)