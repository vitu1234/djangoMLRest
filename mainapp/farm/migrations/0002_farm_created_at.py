# Generated by Django 4.1.5 on 2023-02-01 06:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='farm',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
