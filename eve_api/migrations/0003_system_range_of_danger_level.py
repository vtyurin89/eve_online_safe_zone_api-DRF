# Generated by Django 5.0 on 2023-12-27 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eve_api', '0002_system__danger_level_system_days_researched'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='system',
            constraint=models.CheckConstraint(check=models.Q(('_danger_level__range', (0, 1680))), name='range_of_danger_level'),
        ),
    ]