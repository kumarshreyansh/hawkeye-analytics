from pyexpat import model
from django.contrib import admin
from modelFormsApp.models import ModelClass, CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Additional Info',
            {
                'fields': (
                    'bio',
                    'location',
                    'birth_date',
                    'gender',
                    'weapontype',
                    'coachname',
                    'image',
                )
            }
        )
    )

admin.site.register(ModelClass)
admin.site.register(CustomUser, CustomUserAdmin)