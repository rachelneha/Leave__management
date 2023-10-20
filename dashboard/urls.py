from django.urls import path
from . import views
from dashboard.views import LeaveDasnboardView,HolidayFormCreateView,ProfileView,LeaveStatusView,UserslistView

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('status/<int:pk>', LeaveStatusView.as_view(), name="status"),
    path('userlist/',UserslistView.as_view(), name="userlist"),
    path('holiday/', HolidayFormCreateView.as_view(),name="holiday"),
    path('dashboard/',LeaveDasnboardView.as_view(),name="dashboard"),
    path('profile/', ProfileView.as_view(), name="profile"),
]