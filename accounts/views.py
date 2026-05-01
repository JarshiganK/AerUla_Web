from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import send_mail

from .forms import EmailAuthenticationForm, ResendVerificationForm, SignUpForm
from .tokens import account_activation_token


def account_entry(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    return redirect('accounts:login')


class AccountLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class AccountLogoutView(LogoutView):
    next_page = reverse_lazy('core:home')


def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            verification_url = _send_verification_email(request, user)
            if settings.DEBUG:
                request.session['dev_verification_url'] = verification_url
            return redirect('accounts:verification_sent')
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


def verification_sent(request):
    return render(request, 'accounts/verification_sent.html', {
        'dev_verification_url': request.session.pop('dev_verification_url', ''),
    })


def resend_verification(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = ResendVerificationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email__iexact=email).first()
            if user is not None and not user.is_active:
                verification_url = _send_verification_email(request, user)
                if settings.DEBUG:
                    request.session['dev_verification_url'] = verification_url
                messages.success(
                    request,
                    'We sent a new verification link for that account.',
                )
                return redirect('accounts:verification_sent')

            if user is not None and user.is_active:
                messages.success(request, 'That account is already verified. You can log in now.')
                return redirect('accounts:login')

            messages.success(request, 'If that email has an unverified account, we sent a new verification link.')
            return redirect('accounts:login')
    else:
        form = ResendVerificationForm()

    return render(request, 'accounts/resend_verification.html', {'form': form})


def verify_email(request, uidb64, token):
    user = _get_user_from_uid(uidb64)
    if user is None or not account_activation_token.check_token(user, token):
        messages.error(request, 'This verification link is invalid or has expired.')
        return redirect('accounts:login')

    if user.is_active:
        messages.success(request, 'Your email is already verified. You can log in now.')
        return redirect('accounts:login')

    user.is_active = True
    user.save(update_fields=['is_active'])
    login(request, user)
    messages.success(request, 'Your email has been verified. Welcome to AerUla.')
    return redirect('dashboard:index')


def _send_verification_email(request, user):
    context = {
        'user': user,
        'verification_url': request.build_absolute_uri(
            reverse('accounts:verify_email', kwargs={
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
        ),
    }
    message = render_to_string('accounts/email/verification_email.txt', context)
    send_mail(
        subject='Verify your AerUla account',
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
    return context['verification_url']


def _get_user_from_uid(uidb64):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        return User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return None
