from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterKaryawanForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


class UserCreateForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="-- Pilih Group --"
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "is_active"
        )