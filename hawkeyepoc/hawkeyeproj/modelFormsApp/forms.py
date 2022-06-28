from django.forms import ModelForm
from django import forms
from matplotlib import widgets
from modelFormsApp.models import ModelClass, CustomUser
from django.contrib.auth.forms import UserCreationForm

class FormClass(ModelForm):
    class Meta:
        model = ModelClass
        #fields = '__all__'
        widgets = {
            'matchDate': forms.TextInput(attrs={'type': 'date'}),
            'matchscore': forms.TextInput(attrs={'placeholder': 'Upto 2 decimals'}),
            'higheastseriesscore': forms.TextInput(attrs={'placeholder': 'Upto 2 decimals'}),
            'numberoftens': forms.TextInput(attrs={'placeholder': 'Must be an Integer'}),
            'cancellationofbadshot': forms.TextInput(attrs={'placeholder': 'On a scale of 5'}),
            'stabilityofsightpicture': forms.TextInput(attrs={'placeholder': 'On a scale of 5'}),
            'bodybalance': forms.TextInput(attrs={'placeholder': 'On a scale of 5'}),
            'flowoftheshot': forms.TextInput(attrs={'placeholder': 'On a scale of 5'}),
            'ninetydegreetriggeroperation': forms.TextInput(attrs={'placeholder': 'On a scale of 5'}),
            'averageshotduration': forms.TextInput(attrs={'placeholder': 'On a scale of 5'}),
            'followthrough': forms.TextInput(attrs={'placeholder': 'On a scale of 5'}),
            'visualization': forms.TextInput(attrs={'placeholder': 'On a scale of 5'}),
            'mentalstability': forms.TextInput(attrs={'placeholder': 'On a scale of 5'}),
            'hydrationlevel': forms.TextInput(attrs={'placeholder': 'On a scale of 5'}),
            'fueling': forms.TextInput(attrs={'placeholder': 'On a scale of 5'}),
            'abilityoftheday': forms.TextInput(attrs={'placeholder': 'Enter your details here'}),
            'correctionoftheday': forms.TextInput(attrs={'placeholder': 'Enter your details here'})
            #'planningforthenextpractice': forms.TextInput(attrs={'placeholder': 'Enter your details here'})
        }
        exclude = ['shooterid']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = '__all__'