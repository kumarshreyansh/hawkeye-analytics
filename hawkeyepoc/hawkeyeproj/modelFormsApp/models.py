from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.core.validators import MaxValueValidator, DecimalValidator

from numpy import average


WEAPON_CHOICES = (
    ('1','Rifle'),
    ('0', 'Pistol'),
)

GENDER_CHOICES = (
    ('0','Male'),
    ('1', 'Female'),
)

COACH_CHOICES = (
    ('0','Nandagopal'),
    ('1', 'Sharanendra'),
    ('2', 'Lohith'),
)

SHOT_CHOICES = (
    ('0','40'),
    ('1', '60'),
)

# Create your models here.
class ModelClass(models.Model):
    shooterid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    matchDate = models.DateField(verbose_name="Match Date", max_length=10, blank=False, null=False, default=date.today)
    weekendmatch = models.BooleanField(verbose_name="Weekend Match", default=False)
    totalshots = models.CharField(verbose_name="Total Shots", max_length=1, choices=SHOT_CHOICES, default='0')
    matchscore = models.DecimalField(verbose_name="Match Score", max_digits=5, decimal_places=2)
    higheastseriesscore = models.DecimalField(verbose_name="Higheast Series Score", max_digits=5, decimal_places=2)
    numberoftens = models.IntegerField(verbose_name="Number of Tens", blank=False, null=False)
    cancellationofbadshot = models.IntegerField(verbose_name="Cancellation of Bad Shot", blank=False, null=False, validators=[MaxValueValidator(5)])
    stabilityofsightpicture = models.IntegerField(verbose_name="Stability of Sight Picture", blank=False, null=False, validators=[MaxValueValidator(5)])
    bodybalance = models.IntegerField(verbose_name="Body Balance", blank=False, null=False, validators=[MaxValueValidator(5)])
    flowoftheshot = models.IntegerField(verbose_name="Flow of the Shot", blank=False, null=False, validators=[MaxValueValidator(5)])
    ninetydegreetriggeroperation = models.IntegerField(verbose_name="90&#176; Trigger Operation", blank=False, null=False, validators=[MaxValueValidator(5)])
    averageshotduration = models.IntegerField(verbose_name="Average Shot Duration", blank=False, null=False, validators=[MaxValueValidator(5)])
    followthrough = models.IntegerField(verbose_name="Follow Through", blank=False, null=False, validators=[MaxValueValidator(5)])
    visualization = models.IntegerField(verbose_name="Visualization", blank=False, null=False, validators=[MaxValueValidator(5)])
    mentalstability = models.IntegerField(verbose_name="Mental Stability", blank=False, null=False, validators=[MaxValueValidator(5)])
    hydrationlevel = models.IntegerField(verbose_name="Hydration Level", blank=False, null=False, validators=[MaxValueValidator(5)])
    fueling = models.IntegerField(verbose_name="Fueling", blank=False, null=False, validators=[MaxValueValidator(5)])
    abilityoftheday = models.TextField(verbose_name="Ability of the Day", blank=False, null=False)
    correctionoftheday = models.TextField(verbose_name="Correction of the Day", blank=False, null=False)
    planningforthenextpractice = models.TextField(verbose_name="Next Practice Planning", blank=False, null=False)

    class Meta:
            db_table = 'model_table'
            verbose_name = 'Model Entry'
            verbose_name_plural = 'Model Entries'
    def __str__(self):
        return '{} {}'.format(self.shooterid, self.matchDate)

#text field can't have max_length
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=30)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='1')
    weapontype = models.CharField(max_length=6, choices=WEAPON_CHOICES, default='0')
    coachname = models.CharField(max_length=21, choices=COACH_CHOICES, default='1')
    image = models.ImageField(upload_to='modelFormsApp/static/modelFormsApp/')

    class Meta:
            db_table = 'user_table'
            verbose_name = 'User Entry'
            verbose_name_plural = 'User Entries'



# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(max_length=500, blank=True)
#     location = models.CharField(max_length=30, blank=True)
#     birth_date = models.DateField(null=True, blank=True)
#     gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='1')

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()