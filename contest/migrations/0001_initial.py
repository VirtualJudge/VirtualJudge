# Generated by Django 2.0.5 on 2018-05-12 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('user', models.CharField(max_length=20)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'contest',
                'ordering': ('created_time',),
            },
        ),
        migrations.CreateModel(
            name='ContestProblem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remote_oj', models.CharField(max_length=20)),
                ('remote_id', models.CharField(max_length=20)),
                ('alias', models.CharField(max_length=100, null=True)),
                ('contest_id', models.IntegerField()),
            ],
            options={
                'db_table': 'contest_problem',
                'ordering': ('contest_id',),
            },
        ),
    ]
