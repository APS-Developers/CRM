# Generated by Django 3.2 on 2022-10-14 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_auto_20221013_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalticket',
            name='DeliveryStatus',
            field=models.CharField(blank=True, choices=[('', '---------'), ('Dispatched', 'Dispatched'), ('In Transit', 'In Transit'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered')], max_length=30, verbose_name='Delivery Status'),
        ),
        migrations.AlterField(
            model_name='historicalticket',
            name='DispatchedThrough',
            field=models.CharField(blank=True, choices=[('', '---------'), ('DTDC', 'DTDC'), ('BLUEDART', 'BLUEDART'), ('MARUTI', 'MARUTI'), ('DELHIVERY', 'DELHIVERY'), ('SAFEXPRESS', 'SAFEXPRESS'), ('GATI', 'GATI')], max_length=50, verbose_name='Dispatched through'),
        ),
        migrations.AlterField(
            model_name='historicalticket',
            name='FaultFoundCode',
            field=models.CharField(max_length=100, verbose_name='Fault Found Code'),
        ),
        migrations.AlterField(
            model_name='historicalticket',
            name='ResolutionCode',
            field=models.CharField(blank=True, choices=[('', '---------'), ('Power Issue Resolved with Hard Reset', 'Power Issue Resolved with Hard Reset'), ('External Card Dispatched', 'External Card Dispatched'), ('DRM Issue Resolved', 'DRM Issue Resolved'), ('New Hardware Dispatched', 'New Hardware Dispatched'), ('FAN/Module Dispatched', 'FAN/Module Dispatched'), ('Power Supply Replaced/Dispatched', 'Power Supply Replaced/Dispatched'), ('Booting Issue Resolved', 'Booting Issue Resolved'), ('Console Issues Resolved', 'Console Issues Resolved'), ('Line Card Replaced/Dispatched', 'Line Card Replaced/Dispatched'), ('SUP Card Replaced/Dispatched', 'SUP Card Replaced/Dispatched'), ('Physical Damage - Not covered in AMC', 'Physical Damage - Not covered in AMC'), ('Others', 'Others')], max_length=100, verbose_name='Resolution Code'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='DeliveryStatus',
            field=models.CharField(blank=True, choices=[('', '---------'), ('Dispatched', 'Dispatched'), ('In Transit', 'In Transit'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered')], max_length=30, verbose_name='Delivery Status'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='DispatchedThrough',
            field=models.CharField(blank=True, choices=[('', '---------'), ('DTDC', 'DTDC'), ('BLUEDART', 'BLUEDART'), ('MARUTI', 'MARUTI'), ('DELHIVERY', 'DELHIVERY'), ('SAFEXPRESS', 'SAFEXPRESS'), ('GATI', 'GATI')], max_length=50, verbose_name='Dispatched through'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='FaultFoundCode',
            field=models.CharField(max_length=100, verbose_name='Fault Found Code'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ResolutionCode',
            field=models.CharField(blank=True, choices=[('', '---------'), ('Power Issue Resolved with Hard Reset', 'Power Issue Resolved with Hard Reset'), ('External Card Dispatched', 'External Card Dispatched'), ('DRM Issue Resolved', 'DRM Issue Resolved'), ('New Hardware Dispatched', 'New Hardware Dispatched'), ('FAN/Module Dispatched', 'FAN/Module Dispatched'), ('Power Supply Replaced/Dispatched', 'Power Supply Replaced/Dispatched'), ('Booting Issue Resolved', 'Booting Issue Resolved'), ('Console Issues Resolved', 'Console Issues Resolved'), ('Line Card Replaced/Dispatched', 'Line Card Replaced/Dispatched'), ('SUP Card Replaced/Dispatched', 'SUP Card Replaced/Dispatched'), ('Physical Damage - Not covered in AMC', 'Physical Damage - Not covered in AMC'), ('Others', 'Others')], max_length=100, verbose_name='Resolution Code'),
        ),
    ]
