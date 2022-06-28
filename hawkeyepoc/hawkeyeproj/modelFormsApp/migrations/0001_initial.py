# Generated by Django 4.0.2 on 2022-04-01 05:13

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


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
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('bio', models.TextField(blank=True)),
                ('location', models.CharField(max_length=30)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('0', 'Male'), ('1', 'Female')], default='1', max_length=6)),
                ('weapontype', models.CharField(choices=[('1', 'Rifle'), ('0', 'Pistol')], default='0', max_length=6)),
                ('coachname', models.CharField(choices=[('0', 'Nandagopal'), ('1', 'Sharanendra'), ('2', 'Lohith')], default='1', max_length=21)),
                ('image', models.ImageField(upload_to='modelFormsApp/static/modelFormsApp/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User Entry',
                'verbose_name_plural': 'User Entries',
                'db_table': 'user_table',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ModelClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matchDate', models.DateField(default=datetime.date.today, max_length=10)),
                ('weekendmatch', models.BooleanField(default=False)),
                ('totalshots', models.CharField(choices=[('0', '40'), ('1', '60')], default='0', max_length=1)),
                ('matchscore', models.DecimalField(decimal_places=2, max_digits=5)),
                ('higheastseriesscore', models.DecimalField(decimal_places=2, max_digits=5)),
                ('numberoftens', models.IntegerField()),
                ('cancellationofbadshot', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('stabilityofsightpicture', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('bodybalance', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('flowoftheshot', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('ninetydegreetriggeroperation', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('averageshotduration', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('followthrough', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('visualization', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('mentalstability', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('hydrationlevel', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('fueling', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('abilityoftheday', models.TextField()),
                ('correctionoftheday', models.TextField()),
                ('planningforthenextpractice', models.TextField()),
                ('shooterid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Model Entry',
                'verbose_name_plural': 'Model Entries',
                'db_table': 'model_table',
            },
        ),
    ]
