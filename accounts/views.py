from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from accounts.forms import AccountForm
from accounts.models import Account
from cart.models import Cart
from cart.views import get_cart, _cart_id


# Create your views here.
def register_page(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user  = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.phone_number = phone_number
            user.save()

            # user activation
            current_site = get_current_site(request)
            mail_subject = "Please active your account"
            message = render_to_string("auth/account_verification_email.html", {
                "user": user,
                "domain": current_site,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user)
            })
            to_mail = email
            send_mail = EmailMessage(mail_subject, message, to=[to_mail])
            send_mail.send()

            messages.success(request, "Registration Success! Please check your email")
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = AccountForm()
    context = {
        'form': form
    }
    return render(request, 'auth/register.html', context)


def login_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login success")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')

    return render(request, 'auth/login.html')


@login_required(login_url='login')
def dashboard(request):
    return render(request, "auth/dashboard.html")


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account activate success. Please login")
        return redirect('login')
    else:
        messages.error(request, "Invalid activation link")
        return redirect("register")


# forget password working here
def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        if email is not None:
            exists_email = Account.objects.filter(email=email).exists()
            if exists_email:
                user = Account.objects.get(email__exact=email)
                # user activation
                current_site = get_current_site(request)
                mail_subject = "Reset Your Password"
                message = render_to_string("auth/reset-password-email.html", {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user)
                })
                to_mail = email
                send_mail = EmailMessage(mail_subject, message, to=[to_mail])
                send_mail.send()
                messages.success(request, "Please check your email")
                return redirect('forget-password')
            else:
                messages.error(request, "Account does not exists !")
        else:
            messages.error(request, "Email field is required!")

    return render(request, 'auth/forget-password.html')


def reset_password_validate(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(ValueError, OverflowError, TypeError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, "Please reset your password")
        return redirect('reset-password')
    else:
        messages.error(request, "This link has been expired!")
        return redirect('login')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password and confirm_password is not None:
            # password checking
            if password == confirm_password:
                uid = request.session.get("uid")
                user = Account.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                messages.success(request, "Password Reset Success. Please login")
                return redirect("login")
            else:
                messages.error(request, "Password Does not match")
        else:
            messages.error(request, "Password field is required")

    return render(request, 'auth/reset-password.html')



@login_required(login_url='login')
def logout_page(request):
    logout(request)
    messages.success(request, "You are logged out.")
    return redirect("login")



