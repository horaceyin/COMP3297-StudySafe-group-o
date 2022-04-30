# Generated by Django 4.0.4 on 2022-04-14 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HKUMember',
            fields=[
                ('HKUID', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('venueCode', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=150)),
                ('type', models.CharField(max_length=3)),
                ('capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='VenueEntryExitRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entryDatetime', models.DateTimeField()),
                ('exitDatetime', models.DateTimeField(blank=True)),
                ('duration', models.DurationField(blank=True)),
                ('hkuMember', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StudySafeCore.hkumember')),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StudySafeCore.venue')),
            ],
        ),
        migrations.AddField(
            model_name='venue',
            name='hkuMember',
            field=models.ManyToManyField(through='StudySafeCore.VenueEntryExitRecord', to='StudySafeCore.hkumember'),
        ),
    ]
