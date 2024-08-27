from django import forms
from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import UserCreationForm
from myapp.models import *


class UserRegistrationForm(forms.ModelForm):
    CHOICES = [('user', 'User'), ('artist', 'Artist')]
    role = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            role = self.cleaned_data['role']
            if role == 'artist':
                group = Group.objects.get(name='Artists')
            else:
                group = Group.objects.get(name='Users')
            user.groups.add(group)
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'

class ArtistProfileForm(forms.ModelForm):
    class Meta:
        model = ArtistProfile
        fields ='__all__'

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'

