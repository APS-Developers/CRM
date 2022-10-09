# Generated by Django 3.2 on 2022-10-08 17:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_alter_inventory_item_dispatched_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='Item_dispatched_Date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='Snapshot_Date',
            field=models.DateField(default=datetime.datetime.now, null=True),
        ),
    ]