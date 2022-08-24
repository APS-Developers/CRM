# Generated by Django 3.2 on 2022-08-24 10:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_auto_20220707_0924'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0003_alter_customer_contactno'),
        ('crm', '0009_alter_ticket_onlineresolvable'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='AlternateHW',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.inventory'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='TicketID',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='Ticket ID'),
        ),
        migrations.CreateModel(
            name='HistoricalTicket',
            fields=[
                ('TicketID', models.IntegerField(blank=True, db_index=True, verbose_name='Ticket ID')),
                ('DateCreated', models.DateField(default=django.utils.timezone.now, verbose_name='Date Created')),
                ('Category', models.CharField(max_length=100)),
                ('SubCategory', models.CharField(max_length=100, verbose_name='Sub-Category')),
                ('ModelNo', models.CharField(max_length=100, verbose_name='Model No')),
                ('SerialNo', models.CharField(max_length=100, verbose_name='Serial No')),
                ('Summary', models.TextField(blank=True, max_length=500)),
                ('Priority', models.CharField(blank=True, choices=[('P1', 'P1'), ('P2', 'P2'), ('P3', 'P3'), ('P4', 'P4')], max_length=2)),
                ('AMC', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], null=True)),
                ('Status', models.CharField(blank=True, choices=[('Open', 'Open'), ('Resolved', 'Resolved'), ('Pending', 'Pending'), ('Closed', 'Closed')], max_length=10)),
                ('FaultFoundCode', models.CharField(blank=True, choices=[('Router', 'Router faulty'), ('Modem', 'Modem faulty'), ('Switch', 'Switch faulty')], max_length=30, verbose_name='Fault Found Code')),
                ('ResolutionCode', models.CharField(blank=True, choices=[('123', 'Router faulty'), ('456', 'Modem faulty')], max_length=20, verbose_name='Resolution Code')),
                ('ResolutionRemarks', models.TextField(blank=True, max_length=500, verbose_name='Resolution Remarks')),
                ('OnlineResolvable', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], null=True, verbose_name='Can it be resolved online?')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('AlternateHW', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.inventory')),
                ('Customer', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='customer.customer')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical ticket',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
