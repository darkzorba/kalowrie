import re

from fn.base.decorator import Response
from fn.base.exception import ValidationError
from fn.base.sql import SQLQuery
from core.user.models import User as UserModel
from django.utils import timezone

class User(SQLQuery):
    def __init__(self):
        super().__init__()

    @Response(desc_error="Error creating user.", return_list=['user_id'])
    def create_user(self, email, first_name, last_name, birth_date, password):
        self.validate_password(password)
        new_user_obj = UserModel(email=email, first_name=first_name, last_name=last_name,username=email,
                                 birth_date=birth_date, status=True, is_first_access=True, datm_insert=timezone.now())
        new_user_obj.set_password(password)
        new_user_obj.save()
        return new_user_obj.id


    def validate_password(self, password: str):
        rules = [
            (len(password) >= 8, "Password must be at least 8 characters long."),
            (re.search(r"[A-Z]", password), "Password must contain at least one uppercase letter."),
            (re.search(r"[a-z]", password), "Password must contain at least one lowercase letter."),
            (re.search(r"\d", password), "Password must contain at least one number."),
            (re.search(r"[@$!%*?&]", password), "Password must contain at least one special character (@$!%*?&)."),
        ]

        for passed, message in rules:
            if not passed:
                raise ValidationError(message)