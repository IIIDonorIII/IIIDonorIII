from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Campaign, HouseVisit
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'description']

class HouseVisitForm(forms.ModelForm):
    class Meta:
        model = HouseVisit
        fields = ['campaign', 'house_address']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['birth_date', 'address', 'gender']
