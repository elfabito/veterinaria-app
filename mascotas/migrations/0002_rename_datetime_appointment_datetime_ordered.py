# Generated by Django 4.2.4 on 2024-05-08 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mascotas', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='datetime',
            new_name='datetime_ordered',
        ),
    ]
