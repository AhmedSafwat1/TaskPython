# Generated by Django 2.2.1 on 2019-05-07 21:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doner', '0005_auto_20190507_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blooddonation',
            name='blood_expiration',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 6, 21, 29, 32, 63222), editable=False),
        ),
        migrations.AlterField(
            model_name='blooddonation',
            name='last_donate_date',
            field=models.DateTimeField(),
        ),
    ]
