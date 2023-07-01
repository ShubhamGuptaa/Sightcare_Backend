from django.db import models

# Create your models here.
class Appointment(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    mobile = models.CharField(max_length=13)
    age = models.IntegerField()
    email = models.EmailField(
        verbose_name="email address", 
        max_length=255,
        unique=False
        )
    gender = models.CharField(max_length=3)
    appointment_date = models.CharField(max_length=100,verbose_name="appointment date")
    scheduled_time = models.CharField(max_length=100,verbose_name="scheduled time")
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    ip_address = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return ("Name: "+ self.firstname + " " + self.lastname + ", Appointment Date: " + self.appointment_date)


