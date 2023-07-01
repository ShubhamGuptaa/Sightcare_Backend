from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from clinic.serializer import AppointmentSerializer
from utilities.mixins import ResponseViewMixin
import logging

db_logger = logging.getLogger('db')

class BookAnAppointment(APIView, ResponseViewMixin):
    def post(self, request, format = None):
        try:
            serializer = AppointmentSerializer(data = request.data)
            if serializer.is_valid():
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                ip = ''
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                appointment = serializer.save(ip_address = ip)
                if appointment:
                    email = serializer.data.get("email")
                    mobile = serializer.data.get("mobile")

                    return self.success_response(code = 'HTTP_200_OK', message="Appointment booked successfully!", data = {"Appointment Id: ": appointment.id})
            return self.error_response(code='HTTP_400_BAD_REQUEST', message=serializer.errors)
        except Exception as e:
            db_logger.exception(e)
            print(str(e))
            return self.error_response(code="HTTP_400_BAD_REQUEST",message=str(e))







class TotalCountOFMenuItems(APIView, ResponseViewMixin):
    # permission_classes = [IsAuthenticated]
    def get(self, request, store_id , formate = None):
        try:
            count = 2
            if count:
                return self.success_response(code = 'HTTP_200_OK', message="Total no. of Items with the given Store ID!", data = {'total_items' : count})
            else:
                return self.success_response(code = 'HTTP_200_OK', message="No items found with the given Store ID!")
        except Exception as e:
            db_logger.exception(e)
            print(str(e))
            return self.error_response(code="HTTP_400_BAD_REQUEST",message=f"Invalid Store ID!")