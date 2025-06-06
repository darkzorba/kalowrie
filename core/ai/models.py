from django.db import models

import core.models


# Create your models here.




class AIRoles(core.models.Log):
    base_prompt = models.TextField(null=True)
    chat_name = models.CharField(max_length=255, null=True,unique=True)


    class Meta:
        db_table = '"public"."ai_roles"'