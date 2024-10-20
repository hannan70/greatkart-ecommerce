from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.forms import AccountForm
from accounts.models import Account


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
            account  = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            account.phone_number = phone_number
            account.save()
            messages.success(request, "Registration Success! Please login")
            return redirect('login')
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


def dashboard(request):
    return render(request, "auth/dashboard.html")


def logout_page(request):
    logout(request)
    messages.success(request, "You are logged out.")
    return redirect("login")


