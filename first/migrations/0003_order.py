# Generated by Django 3.1.6 on 2021-04-25 18:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('first', '0002_bike_costperday'),
    ]

    operations = [
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startdaytime', models.DateTimeField()),
                ('enddaytime', models.DateTimeField()),
                ('orderdate', models.DateTimeField(auto_now_add=True)),
                ('bikeid', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='first.bike')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]