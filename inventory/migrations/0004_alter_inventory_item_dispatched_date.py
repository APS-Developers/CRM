# Generated by Django 3.2 on 2022-10-08 17:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_inventory_snapshot_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='Item_dispatched_Date',
            field=models.DateField(default=datetime.datetime.now, null=True),
        ),
    ]