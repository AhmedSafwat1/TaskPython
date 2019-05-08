# Generated by Django 2.2.1 on 2019-05-07 21:28

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Doner', '0004_auto_20190507_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='blooddonation',
            name='last_donate_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blooddonation',
            name='blood_expiration',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 6, 21, 27, 56, 431632), editable=False),
        ),
        migrations.AlterField(
            model_name='blooddonation',
            name='donation_status',
            field=models.CharField(choices=[('1', 'ACCEPT'), ('0', 'REFUSE')], default='1', editable=False, max_length=1),
        ),
        migrations.AlterField(
            model_name='blooddonation',
            name='doner_status',
            field=models.CharField(choices=[('1', 'More Then 3 Month'), ('0', 'Less Then 3 Month')], max_length=1, verbose_name='Last Donate '),
        ),
    ]
