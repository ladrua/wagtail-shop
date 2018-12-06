from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from oscar.core.compat import (
    existing_user_fields, get_user_model)

from oscar.apps.customer.forms import EmailUserCreationForm as CoreEmailUserCreationForm
from oscar.apps.customer.forms import EmailAuthenticationForm as CoreEmailAuthenticationForm
User = get_user_model()

class EmailUserCreationForm(CoreEmailUserCreationForm):
    email = forms.EmailField(label=_('Email address'),widget=forms.TextInput(attrs={'placeholder':'Email address'}))
    password1 = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    password2 = forms.CharField(
        label=_('Confirm password'), widget=forms.PasswordInput(attrs={'placeholder':'Confirm password'}))
    first_name = forms.CharField(
        label=_('First Name'),widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name = forms.CharField(
        label=_('Last Name'),widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    redirect_url = forms.CharField(
        widget=forms.HiddenInput, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class EmailAuthenticationForm(CoreEmailAuthenticationForm):
    username = forms.EmailField(label=_('Email address'),widget=forms.TextInput(attrs={'placeholder':'Email address'}))
    password = forms.CharField(label=_('Password'),widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
