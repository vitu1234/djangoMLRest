# Generated by Django 4.1.5 on 2023-02-02 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0003_userdevice_switch_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdevice',
            name='device_id',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
