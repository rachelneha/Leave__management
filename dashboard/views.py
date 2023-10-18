from django.shortcuts import render, redirect
from django.http import HttpResponse
from dashboard.models import User,Leave,Holidays
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView,DetailView
from dashboard.forms import LeaveForm,HolidayForm

# Create your views here.
def signup(request):
    errors = {}
    if request.method == 'POST':
        username = request.POST['username'].strip()
        firstname = request.POST['firstname'].strip()
        lastname = request.POST['lastname'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()
        password1 = request.POST['password1'].strip()

        if not username:
            errors['username'] = "You must Enter a Username"
        elif len(username) <= 8:
            errors['username'] = "Your username must contain  8 characters"
        else:
            is_present = User.objects.filter(username=username).exists()
            if is_present:
                errors['username'] = "Username exists"
        if not firstname:
            errors['firstname'] = "firstname Required"
        if not password:
            errors['password'] = "Password Required"
        elif len(password) < 8:
            errors['password'] = "Your password must contain  8 characters"
        if not password1:
            errors['password1'] = "Password Required"
        elif len(password1) < 8:
            errors['password1'] = "Your password must contain  8 characters"

        if password and password1 and password != password1:
            errors['password'] = "Password do  not match"

        if not email:
            errors['email'] = "You must enter a email"
        else:
            is_presentt = User.objects.filter(email=email).exists()
            if is_presentt:
                errors['email'] = "email already exit"
        is_valid = len(errors.keys()) == 0
        if is_valid:
            u = User.objects.create_user(
                first_name=firstname,
                last_name=lastname,
                email=email,
                username=username,
                password=password
            )
            u.save()

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/dashboard')
    context = {
        'errors': errors
    }

    return render(request, 'signup.html', context)


def login_view(request):
    errors = {}
    if request.method == "POST":
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()
        if not password:
            errors['password'] = "No password was entered"
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard')
        if user is None:
            errors['InvalidUser_Pass'] ="Invalid UserName or Password"

    context = {
        'errors': errors
    }
    return render(request, 'login.html', context)

class ProfileView(DetailView):
    model = User
    template_name = "userprofile.html"
    context_object_name = "u"

class LeaveDasnboardView(CreateView):
    model = Leave
    form_class = LeaveForm
    template_name = "dashboard.html"
    context_object_name = "leave"


class HolidayFormCreateView(CreateView):
    model = Holidays
    form_class = HolidayForm
    template_name = "holiday.html"
    context_object_name = "Holiday"