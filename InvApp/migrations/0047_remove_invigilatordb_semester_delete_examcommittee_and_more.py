# Generated by Django 4.1.1 on 2023-03-31 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('InvApp', '0046_alter_student_registration_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invigilatordb',
            name='semester',
        ),
        migrations.DeleteModel(
            name='ExamCommittee',
        ),
        migrations.DeleteModel(
            name='InvigilatorDB',
        ),
    ]