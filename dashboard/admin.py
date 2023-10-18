from django.contrib import admin
from .models import User,Holidays,CategoryOfLeave,Leave
# Register your models here.
admin.site.register(User)
admin.site.register(CategoryOfLeave)
admin.site.register(Leave)
admin.site.register(Holidays)