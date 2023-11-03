from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


# Create your models here.
class User(AbstractUser):
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    do_joining = models.DateField(null=True,blank=True)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name

    @receiver(post_save, sender=User)
    def update_user_User(sender, instance, created, **kwargs):
        if created:
            User.objects.create(user=instance)
        instance.User.save()

class CategoryOfLeave(models.Model):

    name = models.CharField(max_length=50)
    total_number = models.IntegerField(null=True)

    def __str__(self):
        return self.name

class Leave(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null = True)
    category_of_leave = models.ForeignKey(CategoryOfLeave,on_delete=models.CASCADE)
    duration_of_leave = models.IntegerField(null=True,blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    STATUS =(
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
             )
    application_status = models.CharField(max_length=50,choices=STATUS,default='Pending', verbose_name ="Update Application Status")
    reason_of_leave = models.TextField(verbose_name ="Reason of name",null = True,help_text="Provide a brief description of the reason for the leave.")

    def __str__(self):
        return self.category_of_leave.name

class Holidays(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField()

    def __str__(self):
        return self.name
