# Generated by Django 4.1.1 on 2023-03-27 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvApp', '0039_alter_teacher_short_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='title',
            field=models.TextField(max_length=400),
        ),
    ]
