# Generated by Django 3.2 on 2021-04-29 12:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('apis', '0002_auto_20210429_1146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='prize',
        ),
        migrations.RemoveField(
            model_name='prize',
            name='winner',
        ),
        migrations.CreateModel(
            name='EventPrize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apis.event')),
                ('prize', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='apis.prize')),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
