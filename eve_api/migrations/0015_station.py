# Generated by Django 5.0 on 2023-12-22 15:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eve_api', '0014_delete_station'),
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('station_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('x', models.FloatField(blank=True, null=True)),
                ('y', models.FloatField(blank=True, null=True)),
                ('z', models.FloatField(blank=True, null=True)),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eve_api.system')),
            ],
        ),
    ]