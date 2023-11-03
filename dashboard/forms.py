from django import forms
from dashboard.models import Leave, Holidays,CategoryOfLeave,User
import re

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields =[
            "category_of_leave","duration_of_leave","start_date","end_date", "reason_of_leave",
                ]

class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holidays
        fields = ["name" ,"date",]

class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ["application_status"]

class LeaveTypeAddForm(forms.ModelForm):
    class Meta:
        model = CategoryOfLeave
        fields = ["name","total_number",]


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["salary","dob","do_joining"]

        labels = {
            "salary": "Add Salary",
            "dob": " Edit Date of Birth",
            "do_joining": "Edit Date of Joining"
        }

class SignupForm(forms.ModelForm):

    password1 = forms.CharField(
        label="Renter the Password",
        widget=forms.PasswordInput,
        help_text="Your password must contain at least 8 characters."
    )

    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User

        fields = [
            "username", "first_name", "last_name", "email", "password", "password1"
        ]


    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise forms.ValidationError("Password must contain at least 8 characters")
        return password

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError("Password must contain at least 8 characters")
        return password1

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not re.search(r'.fegno@gmail.com$', email):
            raise forms.ValidationError("Email must contain '.fegno@gmail.com'")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise forms.ValidationError("You Must need to enter a Username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already in use")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            raise forms.ValidationError("You Must need to enter a first Name")
        return first_name


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password1 = cleaned_data.get("password1")

        if password and password1 and password != password1:
            raise forms.ValidationError("Passwords must match.")

        return cleaned_data