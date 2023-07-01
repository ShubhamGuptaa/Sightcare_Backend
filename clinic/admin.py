from django.contrib import admin

from clinic.models import Appointment

# Register your models here.
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'firstname', 'lastname', 'mobile', 'appointment_date', 'scheduled_time']
    list_filter = ('appointment_date', 'scheduled_time')
    search_fields = ('appointment_date', 'scheduled_time')

    fieldsets = (
        ('Patient Details', {'fields': ('firstname','lastname', 'mobile', 'email', 'age', 'gender',)}),
        ('Appointment Details', {'fields': ('appointment_date','scheduled_time',)}),
        ('Address Details',{'fields': ('address','city',)}),
    )

admin.site.register(Appointment,AppointmentAdmin)
