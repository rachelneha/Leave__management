from django.shortcuts import render, redirect
from django.http import HttpResponse
from dashboard.models import User,Leave,Holidays
from django.contrib.auth import authenticate, login,logout
from django.views.generic import CreateView,DetailView,ListView
from dashboard.forms import LeaveForm,HolidayForm,StatusUpdateForm
from django.db.models import Count

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

    def get_object(self):
        return self.request.user


class LeaveDasnboardView(CreateView):
    model = Leave
    form_class = LeaveForm
    template_name = "dashboard.html"
    #context_object_name = "leave"
    success_url = '/status/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Leave_count = Leave.objects.values('category_of_leave__name','category_of_leave__total_number').annotate(total=Count('category_of_leave__name'))
        Leavee = Leave.objects.all()
        context['leave'] = Leavee
        context['leave_count'] = Leave_count

        return context


class UserslistView(ListView):
    model = User
    template_name = "alluserslist.html"
    context_object_name = "userd"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['userd'] = User.objects.all()
    #     return context



class HolidayFormCreateView(CreateView):
    model = Holidays
    form_class = HolidayForm
    template_name = "holiday.html"
    context_object_name = "Holiday"
    success_url='/holiday/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['holiday_list'] = Holidays.objects.all()
        return context

def logout_view(request):
    logout(request)
    return redirect('/')


class LeaveStatusView(ListView):
    model = Leave
    template_name = "leavestatus.html"
    form_class = StatusUpdateForm

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return Leave.objects.filter(user_id=user_id)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['pk']
        context['employee'] = User.objects.get(id=user_id)

        if self.request.method == 'POST':

            form = StatusUpdateForm(self.request.POST)
            if form.is_valid():

                form.save()

                return redirect('status')

        return context