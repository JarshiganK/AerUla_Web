from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .roles import ROLE_VENDOR, ROLE_VIEWER, assign_role


class EmailAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            'Please enter a correct email address and password. '
            'Note that both fields may be case-sensitive.'
        ),
        'inactive': 'Your account is not verified yet. Please open the verification link sent to your email.',
    }

    username = forms.EmailField(
        label='Email address',
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'class': 'form-control',
        }),
    )

    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': 'form-control',
        }),
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            inactive_user = User.objects.filter(username__iexact=username, is_active=False).first()
            if inactive_user is not None and inactive_user.check_password(password):
                raise ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )

            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class SignUpForm(UserCreationForm):
    ACCOUNT_VIEWER = ROLE_VIEWER
    ACCOUNT_VENDOR = ROLE_VENDOR
    ACCOUNT_TYPE_CHOICES = [
        (ACCOUNT_VIEWER, 'Viewer - explore huts, badges, bookings, and products'),
        (ACCOUNT_VENDOR, 'Vendor - add and manage cultural experiences'),
    ]

    first_name = forms.CharField(
        label='First name',
        max_length=150,
        widget=forms.TextInput(attrs={
            'autocomplete': 'given-name',
            'class': 'form-control',
        }),
    )
    email = forms.EmailField(
        label='Email address',
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'class': 'form-control',
        }),
    )
    account_type = forms.ChoiceField(
        label='Account type',
        choices=ACCOUNT_TYPE_CHOICES,
        initial=ACCOUNT_VIEWER,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        help_text='Choose vendor only if you will provide bookable cultural experiences.',
    )

    class Meta:
        model = User
        fields = ('first_name', 'email', 'account_type', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ('password1', 'password2'):
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
            })

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists() or User.objects.filter(username__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean_account_type(self):
        return self.cleaned_data.get('account_type') or self.ACCOUNT_VIEWER

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.is_active = False
        if commit:
            user.save()
            assign_role(user, self.cleaned_data['account_type'])
        return user


class ResendVerificationForm(forms.Form):
    email = forms.EmailField(
        label='Email address',
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'class': 'form-control',
        }),
    )

    def clean_email(self):
        return self.cleaned_data['email'].strip().lower()
