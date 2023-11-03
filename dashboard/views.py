from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from dashboard.models import User, Leave, Holidays, CategoryOfLeave
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, DetailView, ListView, FormView, UpdateView
from dashboard.forms import LeaveForm, HolidayForm, StatusUpdateForm, LeaveTypeAddForm, EditUserForm,SignupForm
from django.db.models import Count, Sum
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.contrib.sites.shortcuts import get_current_site
#from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from dashboard.tokens import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.core.mail import send_mail

#from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from dashboard.tokens import account_activation_token


# Create your views here.
# def signup(request):
#     errors = {}
#     if request.method == 'POST':
#         username = request.POST['username'].strip()
#         firstname = request.POST['firstname'].strip()
#         lastname = request.POST['lastname'].strip()
#         email = request.POST['email'].strip()
#         password = request.POST['password'].strip()
#         password1 = request.POST['password1'].strip()
#
#         if not username:
#             errors['username'] = "You must Enter a Username"
#         elif len(username) <= 8:
#             errors['username'] = "Your username must contain  8 characters"
#         else:
#             is_present = User.objects.filter(username=username).exists()
#             if is_present:
#                 errors['username'] = "Username exists"
#         if not firstname:
#             errors['firstname'] = "firstname Required"
#         if not password:
#             errors['password'] = "Password Required"
#         elif len(password) < 8:
#             errors['password'] = "Your password must contain  8 characters"
#         if not password1:
#             errors['password1'] = "Password Required"
#         elif len(password1) < 8:
#             errors['password1'] = "Your password must contain  8 characters"
#
#         if password and password1 and password != password1:
#             errors['password'] = "Password do  not match"
#
#         if not email:
#             errors['email'] = "You must enter a email"
#         else:
#             is_presentt = User.objects.filter(email=email).exists()
#             if is_presentt:
#                 errors['email'] = "email already exit"
#         is_valid = len(errors.keys()) == 0
#         if is_valid:
#             u = User.objects.create_user(
#                 first_name=firstname,
#                 last_name=lastname,
#                 email=email,
#                 username=username,
#                 password=password
#             )
#             u.save()
#
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             return redirect('/dashboard')
#     context = {
#         'errors': errors
#     }
#
#     return render(request, 'signup.html', context)

class SignupView(FormView):
    model = User
    template_name = "signupp.html"
    form_class=SignupForm
    success_url = '/dashboard/'

    def form_valid(self,form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        subject = 'Confirm to create an Account in Leavecom'
        message = render_to_string('account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(str(user.pk).encode()),
            'token': account_activation_token.make_token(user),
        })


        user.email_user(subject, message)
        # from_email = 'neharachel18@gmail.com'
        # email = form.cleaned_data['email']
        # recipient_list = [email]
        # send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return redirect('account_activation_sent')


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        # username = form.cleaned_data['username']
        # password = form.cleaned_data['password']
        # authenticated_user = authenticate(username=username, password=password)
        #
        # if authenticated_user:
        #      login(self.request, authenticated_user)

        return redirect('/dashboard')
    else:
        return render(request, 'account_activation_invalid.html')

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
            errors['InvalidUser_Pass'] = "Invalid UserName or Password"

    context = {
        'errors': errors
    }
    return render(request, 'login.html', context)


@method_decorator(login_required, name='dispatch')
class ProfileView(DetailView):
    model = User
    template_name = "userprofile.html"
    context_object_name = "u"

    def get_object(self):
        user = self.request.user
        return user


@method_decorator(login_required, name='dispatch')
class AddDetails(UpdateView):
    model = User
    template_name = "addDetail.html"
    context_object_name = "u"
    form_class = EditUserForm
    success_url='/userlist/'


@method_decorator(login_required, name='dispatch')
class LeaveDasnboardView(CreateView):
    model = Leave
    form_class = LeaveForm
    template_name = "dashboard.html"
    # context_object_name = "leave"
    success_url = '/dashboard/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Leave_count = Leave.objects.filter(user=self.request.user,
                                           application_status__in=['Approved', 'Pending']).values(
            'category_of_leave').annotate(consumed=Sum('duration_of_leave'))
        Leave.objects.filter(application_status__in=['Pending']).values('category_of_leave').annotate(
            pending=Count('id'))

        leave_dict = {}
        for lleave in Leave_count:
            key = lleave['category_of_leave']
            leave_dict[key] = lleave['consumed']
        new_list = []
        for category in CategoryOfLeave.objects.values("id", "name", "total_number"):
            if category['id'] in leave_dict:
                new_dict = {}
                total_number = category['total_number']
                consumed = leave_dict[category['id']]
                new_dict['name'] = category['name']
                new_dict['total_number'] = total_number
                new_dict['remaining_days'] = total_number - consumed
                new_dict['consumed'] = consumed
                new_list.append(new_dict)

        Leavee = Leave.objects.filter(user=self.request.user)
        context['leave'] = Leavee
        context['leave_count'] = Leave_count
        context['new_list'] = new_list

        return context


@method_decorator(login_required, name='dispatch')
class UserslistView(ListView):
    model = User
    template_name = "alluserslist.html"
    context_object_name = "userd"


@method_decorator(login_required, name='dispatch')
class HolidayFormCreateView(CreateView):
    model = Holidays
    form_class = HolidayForm
    template_name = "holiday.html"
    context_object_name = "Holiday"
    success_url = '/holiday/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['holiday_list'] = Holidays.objects.all()
        return context


def logout_view(request):
    logout(request)
    return redirect('/')


@method_decorator(login_required, name='dispatch')
class AdminStatusUpdate(ListView):
    model = Leave
    template_name = "AdminUpdate.html"
    form_class = StatusUpdateForm
    success_url = '/update/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = User.objects.all()
        context['object_list'] = Leave.objects.filter(application_status='Pending').order_by('-id')
        return context


@method_decorator(login_required, name='dispatch')
class UpdateView(UpdateView):
    model = Leave
    template_name = "Update.html"
    form_class = StatusUpdateForm
    success_url = '/update/'


@method_decorator(login_required, name='dispatch')
class LeaveStatusView(UpdateView):
    model = Leave
    template_name = "leavestatus.html"
    form_class = StatusUpdateForm

    def get_success_url(self):
        return reverse_lazy('status', kwargs={"pk": self.kwargs["pk"]})

    def get_object(self):
        if self.request.method == "POST":
            pk = self.request.POST.get('pk')
            return get_object_or_404(Leave, pk=pk)
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['pk']
        context['employee'] = User.objects.get(id=user_id)
        user_id = self.kwargs['pk']
        context['object_list'] = Leave.objects.filter(user_id=user_id).order_by('-id')
        return context


@method_decorator(login_required, name='dispatch')
class LeaveTypeView(CreateView):
    model = CategoryOfLeave
    from_class = LeaveTypeAddForm
    template_name = "leavetypes.html"
    success_url = '/dashboard/'
    fields = ["name", "total_number", ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = CategoryOfLeave.objects.all()
        return context
