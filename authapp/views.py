from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm, ShopUserProfileForm
from authapp.models import User
from basketapp.models import Basket

def send_verify_email(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    subject = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения перейдите по ссылке {settings.DOMAIN}/{verify_link}'

    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.activation_key = None
            user.save()
            auth.login(request, user)
        return render(request, 'authapp/verification.html')
    except Exception as ex:
        return HttpResponseRedirect(reverse('main'))



def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main'))
    else:
        form = UserLoginForm()

    context = {'form': form}

    return render(request, 'authapp/login.html', context)


def register(request):    
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            send_verify_email(user)
            messages.success(request, 'Письмо с кодом активации отправлено вам на почту')
            return HttpResponseRedirect(reverse('authapp:login'))
    else:
        form = UserRegisterForm()    

    context = {'form': form}

    return render(request, 'authapp/register.html', context)

def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = ShopUserProfileForm(data=request.POST, instance=request.user.shopuserprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('authapp:profile'))
    else:
        form = UserProfileForm(instance=request.user)
        profile_form = ShopUserProfileForm(instance=request.user.shopuserprofile)

    context = {
        'form': form,
        'profile_form': profile_form
    }

    return render(request, 'authapp/profile.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))