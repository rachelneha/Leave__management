from django.urls import path
from . import views
from dashboard.views import LeaveDasnboardView,HolidayFormCreateView,ProfileView

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('', views.login_view, name="login"),
    path('holiday/', HolidayFormCreateView.as_view(),name="holiday"),
    path('dashboard/',LeaveDasnboardView.as_view(),name="dashboard"),
    path('profile/<int:pk>', ProfileView.as_view(), name="profile"),
]