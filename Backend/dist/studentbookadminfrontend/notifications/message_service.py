import random
from django.utils import timezone 
from studentbookadminbackend import settings
from twilio.rest import Client
from studentbookadminfrontend.views.dashboard_views import api_response
from rest_framework import status


def send_otp_newphone_number(user,subject_type,new_phone_number, phone_number_field="phone_number"):
    """
    Generates an OTP, saves it to user, and sends an email.
    Works for Student/User model that has fields: otp, otp_created_at
    """
 
    # 1. Generate OTP
    otp = str(random.randint(100000, 999999))
    user.otp = otp
    user.otp_created_at = timezone.now()
    user.save()
    phone_number = getattr(user, phone_number_field)
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Your OTP is: {otp} for {subject_type}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to='+91'+str(new_phone_number)
        )
        return api_response(
                message=f"For Change Phone Number on School Book an OTP sent to {new_phone_number}",
                message_type="success",
                status_code=status.HTTP_200_OK,
            )
 
    except Exception as e:
        # return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return api_response(
                message=str(e),
                message_type="error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )