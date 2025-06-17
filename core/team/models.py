from django.db import models

import core.models


# Create your models here.




class Team(core.models.Log):
    name = models.CharField(max_length=100, null=True)
    team_color = models.CharField(max_length=50, null=True)
    team_logo = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = u'"public"."team"'


class TeamAdmin(core.models.Log):
    team = models.ForeignKey('team.Team', on_delete=models.DO_NOTHING, null=True)
    user = models.ForeignKey('user.User', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = u'"public"."team_admin"'
