# Generated by Django 3.2 on 2022-10-09 18:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0005_auto_20221008_2248"),
    ]

    operations = [
        migrations.AlterField(
            model_name="inventory",
            name="Snapshot_Date",
            field=models.DateField(null=True),
        ),
    ]
