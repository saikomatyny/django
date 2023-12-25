from django.db import models

class todolists(models.Model):
    name_of_task = models.CharField('Что нужно сделать: ', max_length = 100)
    if_complete = models.BooleanField('Сделано или нет')


    def __str__(self):
        return self.name_of_task
    
    class Meta:
        verbose_name = 'Список дел'