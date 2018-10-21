# Generated by Django 2.0.5 on 2018-05-12 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.CharField(max_length=20)),
                ('contest_id', models.IntegerField(null=True)),
                ('code', models.TextField()),
                ('language', models.CharField(max_length=20)),
                ('language_name', models.CharField(max_length=30, null=True)),
                ('remote_oj', models.CharField(max_length=20, null=True)),
                ('remote_id', models.CharField(max_length=20, null=True)),
                ('remote_run_id', models.CharField(max_length=20, null=True)),
                ('verdict', models.CharField(max_length=40, null=True)),
                ('verdict_code', models.IntegerField(default=0)),
                ('execute_time', models.CharField(max_length=20, null=True)),
                ('execute_memory', models.CharField(max_length=20, null=True)),
                ('compile_info', models.TextField(null=True)),
                ('status', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'submission',
                'ordering': ('-create_time',),
            },
        ),
    ]
