# Generated by Django 3.2 on 2022-10-11 02:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_auto_20221010_0008'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalticket',
            old_name='AlternateHW',
            new_name='HWDispatched',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='AlternateHW',
            new_name='HWDispatched',
        ),
    ]
