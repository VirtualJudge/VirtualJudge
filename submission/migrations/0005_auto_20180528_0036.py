# Generated by Django 2.0.5 on 2018-05-27 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0004_remove_submission_contest_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='verdict',
            field=models.CharField(default='waiting', max_length=40, null=True),
        ),
    ]
