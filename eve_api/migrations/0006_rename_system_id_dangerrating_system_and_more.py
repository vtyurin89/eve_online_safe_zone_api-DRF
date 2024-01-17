# Generated by Django 5.0 on 2024-01-09 11:24

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eve_api', '0005_dangerrating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dangerrating',
            old_name='system_id',
            new_name='system',
        ),
        migrations.AlterField(
            model_name='dangerrating',
            name='rating_id',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]