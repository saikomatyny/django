from django.db import models

class todolists(models.Model):
    name_of_task = ''
    if_complete = bool
