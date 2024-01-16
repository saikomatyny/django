from django.db import models

class nameOfList(models.Model):
    name_of_list = models.CharField('Название списка ваших дел: ', max_length=100)

    def __str__(self):
        return self.name_of_list
    
    class Meta:
        verbose_name_plural, verbose_name = 'Списки дел', 'Списки дел'

class todolist(models.Model):

    name_of_task = models.CharField('Что нужно сделать: ', max_length=100)
    done_or_not = models.BooleanField('Сделано или нет: ')

    lists_of_todolist = models.ManyToManyField(nameOfList, related_name='tasks')


    def __str__(self):
        return self.name_of_task
    
    class Meta:
        verbose_name_plural, verbose_name = 'Список дел', 'Список дел'
