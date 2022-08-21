# Generated by Django 3.2 on 2022-07-06 06:17

from django.db import migrations, models
import inventory.validators


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0005_alter_inventory_organisation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="inventory",
            name="Slip",
            field=models.FileField(
                default=None,
                null=True,
                upload_to="",
                validators=[inventory.validators.validate_file_extension],
            ),
        ),
    ]
