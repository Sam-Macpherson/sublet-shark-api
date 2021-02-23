# Generated by Django 3.1.3 on 2020-12-16 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_auto_20201202_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='end_date',
            field=models.DateField(help_text='The day by which the subletter must leave.'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='start_date',
            field=models.DateField(help_text='The first day that the subletter may move in.'),
        ),
    ]