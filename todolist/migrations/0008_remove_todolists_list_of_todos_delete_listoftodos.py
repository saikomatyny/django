# Generated by Django 5.0 on 2024-01-14 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0007_listoftodos_delete_valuemodel_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todolists',
            name='list_of_todos',
        ),
        migrations.DeleteModel(
            name='ListOfToDos',
        ),
    ]
