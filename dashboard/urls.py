from django.urls import path,re_path
from . import views
from dashboard.views import LeaveDasnboardView,HolidayFormCreateView,ProfileView,LeaveStatusView,UserslistView,LeaveTypeView,AddDetails,AdminStatusUpdate,UpdateView,SignupView
urlpatterns = [
    path('signup/', SignupView.as_view(), name="signup"),
    path('', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('status/<int:pk>/', LeaveStatusView.as_view(), name="status"),
    path('update/', AdminStatusUpdate.as_view(), name="update"),
    path('updateRequest/<int:pk>/', UpdateView.as_view(), name="request"),
    path('userlist/',UserslistView.as_view(), name="userlist"),
    path('holiday/', HolidayFormCreateView.as_view(),name="holiday"),
    path('dashboard/',LeaveDasnboardView.as_view(),name="dashboard"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('leavetype/', LeaveTypeView.as_view(), name="leavetype"),
    path('editdetails/<int:pk>/', AddDetails.as_view(), name="editdetails"),

    path("account_activation_sent/", views.account_activation_sent, name='account_activation_sent'),
    #path("activate/?P<uidb64>[0-9A-Za-z_\-]+/?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}/", views.activate, name='activate'),
    path("activate/<uidb64>/<token>/", views.activate, name='activate'),

]