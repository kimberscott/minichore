# Generated by Django 2.0.7 on 2018-07-30 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allocate', '0011_auto_20180727_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='household',
            name='allocationProgress',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='household',
            name='completedAllocations',
            field=models.BooleanField(default=False),
        ),
    ]
