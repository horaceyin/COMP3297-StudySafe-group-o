# Generated by Django 4.0.4 on 2022-04-14 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudySafeCore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venueentryexitrecord',
            name='duration',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='venueentryexitrecord',
            name='exitDatetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
