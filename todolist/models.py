from django.db import models

class todolists(models.Model):
    name_of_task = models.CharField('Что нужно сделать: ', max_length = 100)
    done_or_not = models.BooleanField('Сделано или нет')


    def __str__(self):
        return self.name_of_task
    
    class Meta:
        verbose_name_plural, verbose_name = 'Список дел', 'Список дел'