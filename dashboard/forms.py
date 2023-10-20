from django import forms
from dashboard.models import Leave, Holidays

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields =[
            "category_of_leave","duration_of_leave","start_date","end_date", "reason_of_leave",
                ]

class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holidays
        fields = ["name" ,"date"]

class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ["application_status"]