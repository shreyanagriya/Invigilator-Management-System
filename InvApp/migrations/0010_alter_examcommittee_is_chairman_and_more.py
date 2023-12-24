# Generated by Django 4.1.2 on 2022-10-22 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('InvApp', '0009_examcommittee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examcommittee',
            name='is_chairman',
            field=models.CharField(choices=[{'NafisSarker-( NS )', 'NS'}], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='examcommittee',
            name='teacher',
            field=models.ForeignKey(choices=[{'NafisSarker-( NS )', 'NS'}], on_delete=django.db.models.deletion.CASCADE, to='InvApp.teacher'),
        ),
    ]
