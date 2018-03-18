from user_profile.models import UserProfile
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileModelForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('image', 'bio', 'location')


class UserDetailModelForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name',)
