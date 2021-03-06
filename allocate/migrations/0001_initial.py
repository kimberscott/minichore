# Generated by Django 2.0.7 on 2018-07-16 15:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Allocation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this allocation', primary_key=True, serialize=False)),
            ],
            options={
                'ordering': ['household'],
            },
        ),
        migrations.CreateModel(
            name='Chore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the name of a chore', max_length=40)),
            ],
            options={
                'ordering': ['household', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Doer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the name of a household member', max_length=40)),
                ('hasWeights', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Household',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this household', primary_key=True, serialize=False)),
                ('allocations_are_current', models.BooleanField(default=False)),
                ('name', models.CharField(help_text="Enter a name for the household (e.g., 'The Scotts')", max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Weight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('chore', models.ForeignKey(on_delete='CASCADE', to='allocate.Chore')),
                ('doer', models.ForeignKey(on_delete='CASCADE', to='allocate.Doer')),
            ],
            options={
                'ordering': ['doer', 'chore'],
            },
        ),
        migrations.AddField(
            model_name='doer',
            name='household',
            field=models.ForeignKey(on_delete='CASCADE', to='allocate.Household'),
        ),
        migrations.AddField(
            model_name='chore',
            name='doer',
            field=models.ForeignKey(on_delete='CASCADE', to='allocate.Doer'),
        ),
        migrations.AddField(
            model_name='chore',
            name='household',
            field=models.ForeignKey(on_delete='CASCADE', to='allocate.Household'),
        ),
        migrations.AddField(
            model_name='allocation',
            name='assignments',
            field=models.ManyToManyField(help_text='Weights for all doers for the chores they are assigned', to='allocate.Weight'),
        ),
        migrations.AddField(
            model_name='allocation',
            name='household',
            field=models.ForeignKey(on_delete='CASCADE', to='allocate.Household'),
        ),
    ]
