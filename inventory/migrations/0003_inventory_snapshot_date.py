# Generated by Django 3.2 on 2022-10-08 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0002_rename_slip_inventory_cli_snapshot"),
    ]

    operations = [
        migrations.AddField(
            model_name="inventory",
            name="Snapshot_Date",
            field=models.DateField(null=True),
        ),
    ]
