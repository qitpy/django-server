# Generated by Django 4.1.3 on 2022-11-28 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_todomonth_tasks_remove_todoschedule_task_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todocard',
            name='is_done',
        ),
        migrations.RemoveField(
            model_name='tododaily',
            name='is_done',
        ),
        migrations.RemoveField(
            model_name='todomonth',
            name='is_done',
        ),
        migrations.RemoveField(
            model_name='todoschedule',
            name='is_done',
        ),
        migrations.RemoveField(
            model_name='todoyear',
            name='is_done',
        ),
    ]
