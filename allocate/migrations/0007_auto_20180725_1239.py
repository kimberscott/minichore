# Generated by Django 2.0.7 on 2018-07-25 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allocate', '0006_auto_20180725_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weight',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
