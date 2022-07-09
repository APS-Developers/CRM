# Generated by Django 3.2 on 2022-07-06 05:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_alter_customer_contactno'),
        ('inventory', '0003_remove_inventory_orgid'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='Organisation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='customer.organisation'),
        ),
    ]
