# Generated by Django 4.2.4 on 2024-04-27 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mascotas', '0004_alter_mascota_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mascota',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
