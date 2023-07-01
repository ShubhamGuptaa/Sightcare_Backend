from rest_framework import serializers

from clinic.models import Appointment
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['firstname', 'lastname', 'mobile', 'age','email', 'gender', 'appointment_date', 'scheduled_time', 'address', 'city', ]


    # validating password and confirm password
    def validate(self, attrs):
        return attrs