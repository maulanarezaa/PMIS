from django import forms
from .models import Role, Permission

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['nama']


class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['nama', 'kode']