# Generated by Django 4.1.1 on 2023-03-25 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvApp', '0038_alter_course_course_name_alter_exam_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='short_name',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]