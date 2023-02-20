# Generated by Django 3.2 on 2022-10-13 11:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("crm", "0005_merge_0003_auto_20221011_0755_0004_auto_20221012_1257"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalticket",
            name="DeliveryStatus",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "---------"),
                    ("Dispatched", "Dispatched"),
                    ("Delivered", "Delivered"),
                ],
                max_length=30,
                verbose_name="Delivery Status",
            ),
        ),
        migrations.AlterField(
            model_name="historicalticket",
            name="DispatchedThrough",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "---------"),
                    ("Delhivery", "Delhivery"),
                    ("Blue Dart", "Blue Dart"),
                ],
                max_length=50,
                verbose_name="Dispatched through",
            ),
        ),
        migrations.AlterField(
            model_name="historicalticket",
            name="OnlineResolvable",
            field=models.CharField(
                blank=True,
                choices=[("", "---------"), ("Yes", "Yes"), ("No", "No")],
                max_length=10,
                verbose_name="Online Resolvable",
            ),
        ),
        migrations.AlterField(
            model_name="historicalticket",
            name="ResolutionCode",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "---------"),
                    ("123", "Router faulty"),
                    ("456", "Modem faulty"),
                ],
                max_length=20,
                verbose_name="Resolution Code",
            ),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="DeliveryStatus",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "---------"),
                    ("Dispatched", "Dispatched"),
                    ("Delivered", "Delivered"),
                ],
                max_length=30,
                verbose_name="Delivery Status",
            ),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="DispatchedThrough",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "---------"),
                    ("Delhivery", "Delhivery"),
                    ("Blue Dart", "Blue Dart"),
                ],
                max_length=50,
                verbose_name="Dispatched through",
            ),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="OnlineResolvable",
            field=models.CharField(
                blank=True,
                choices=[("", "---------"), ("Yes", "Yes"), ("No", "No")],
                max_length=10,
                verbose_name="Online Resolvable",
            ),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="ResolutionCode",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "---------"),
                    ("123", "Router faulty"),
                    ("456", "Modem faulty"),
                ],
                max_length=20,
                verbose_name="Resolution Code",
            ),
        ),
    ]
