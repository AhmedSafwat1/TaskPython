# Generated by Django 2.2.1 on 2019-05-09 20:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doner', '0010_auto_20190508_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blooddonation',
            name='blood_expiration',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 8, 20, 1, 16, 245027), editable=False),
        ),
        migrations.AlterField(
            model_name='blooddonation',
            name='description',
            field=models.TextField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='blooddonation',
            name='doner_status',
            field=models.CharField(choices=[('1', 'More Then 3 Month'), ('0', 'Less Then 3 Month')], default='1', editable=False, max_length=1, verbose_name='Last Donate '),
        ),
        migrations.AlterField(
            model_name='blooddonation',
            name='test_state',
            field=models.CharField(choices=[('0', 'NAGATIVE'), ('1', 'PPSTIVE')], max_length=1, verbose_name='Virus Test'),
        ),
    ]
