# Generated by Django 3.2 on 2022-07-07 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0008_alter_ticket_amc"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="OnlineResolvable",
            field=models.BooleanField(
                choices=[(True, "Yes"), (False, "No")],
                null=True,
                verbose_name="Can it be resolved online?",
            ),
        ),
    ]
