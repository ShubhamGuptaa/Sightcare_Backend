from django.contrib import admin
from django.urls import path, include

from clinic.views import BookAnAppointment

urlpatterns = [
    path('appointment', BookAnAppointment.as_view(), name="book an appointment"),
   

]
