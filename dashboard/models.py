from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    dob = models.DateField(null=True)
    do_joining = models.DateField(null=True)

    def __str__(self):
        return self.first_name

class Category_of_leave(models.Model):
    name = models.CharField(max_length=20)
    total_number = models.IntegerField(null=True)

    def __str__(self):
        return self.name

class Leave(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category_of_leave = models.ForeignKey(Category_of_leave,on_delete=models.CASCADE)
    duration_of_leave = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    STATUS =(
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
             )
    application_status = models.CharField(max_length=50,choices=STATUS,default='Pending')

    def __str__(self):
        return self.category_of_leave

class Holidays(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField()

    def __str__(self):
        return self.name
