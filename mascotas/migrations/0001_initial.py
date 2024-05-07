# Generated by Django 4.2.4 on 2024-05-07 01:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mascotas.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_veterinario', models.BooleanField(default=False)),
                ('is_provedor', models.BooleanField(default=False)),
                ('email', models.EmailField(db_index=True, max_length=250, unique=True)),
                ('dni', models.CharField(blank=True, max_length=8, null=True, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', mascotas.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('precio', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Provedor',
            fields=[
                ('idProvedor', models.AutoField(primary_key=True, serialize=False)),
                ('razonSocial', models.TextField(max_length=30)),
                ('rut', models.TextField(blank=True, null=True)),
                ('domicilio', models.TextField(blank=True, max_length=255, null=True)),
                ('telefono', models.TextField(blank=True, max_length=25, null=True)),
                ('provedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='provedor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('idProducto', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('precio', models.IntegerField()),
                ('cantidad', models.IntegerField(default=1)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mascotas.category')),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mascotas.provedor')),
            ],
        ),
        migrations.CreateModel(
            name='Mascota',
            fields=[
                ('idMascota', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, max_length=17)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('especie', models.CharField(blank=True, max_length=17)),
                ('raza', models.CharField(blank=True, max_length=100)),
                ('edad', models.IntegerField()),
                ('fechaNac', models.DateField()),
                ('propietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mascota', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HistoriaMedica',
            fields=[
                ('idHistoria', models.AutoField(primary_key=True, serialize=False)),
                ('fechaConsulta', models.DateTimeField(auto_now_add=True)),
                ('diagnostico', models.TextField(max_length=255)),
                ('tratamiento', models.TextField(max_length=255)),
                ('mascota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mascotas.mascota')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField()),
                ('comment', models.TextField(blank=True)),
                ('time_ordered', models.DateTimeField(auto_now_add=True)),
                ('canceled', models.BooleanField(default=False)),
                ('approved', models.BooleanField(default=False)),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mascotas.service')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
