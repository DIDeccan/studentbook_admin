from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from datetime import datetime
from ipware import get_client_ip # (pip install django-ipware)
from studentbookadminfrontend.models import *
from studentbookadminfrontend.views.dashboard_views import api_response
import random
from studentbookadminfrontend.notifications.message_service import *
User = get_user_model()

class UserDetailsAPIView(APIView):
    def get(self, request):
        students = Student.objects.all()
        class_filter = request.query_params.get('class')
        status_filter = request.query_params.get('status')
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        if class_filter:
            class_name = Class.objects.filter(id = class_filter).first()
            print(class_name)
            if class_name is None:
                    print("hi")
                    return api_response(
                        message="No class avilable",
                        message_type="error",
                        status_code=status.HTTP_400_BAD_REQUEST
               
                    )
            students = students.filter(student_class=class_filter)
        if status_filter:
            # is_active = status_filter.lower() == 'active'
            # students = students.filter(is_active=is_active)
            if status_filter == 'active':
                students = students.filter(is_active=True)
            elif status_filter == 'inactive':
                students = students.filter(is_active=False)
        if start_date_str and end_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                students = students.filter(registered_date__date__range=[start_date, end_date])
            except ValueError:
                return api_response("Invalid date format. Use YYYY-MM-DD.", "error", status.HTTP_400_BAD_REQUEST)

    
        user_details_data = []
        for student in students:
            last_login_time = student.login_time.strftime('%Y-%m-%d %H:%M:%S') if student.login_time else "N/A"
            subscription_info = "No Subscription"
            try:
                subscription = student.subscription_orders.filter(payment_status='completed').first()
                if subscription:
                    subscription_info = f"{subscription.course.name} - Paid: {subscription.price}"
            except SubscriptionOrder.DoesNotExist:
                pass
            user_details_data.append({
                'name': f"{student.first_name} {student.last_name}",
                'email': student.email,
                'phone': student.phone_number,
                'registered_class': student.student_class.name,
                'registered_date': student.registered_date.date(),
                'status': "Active" if student.is_active else "Inactive",
                'profile_picture': student.profile_image.url if student.profile_image else None,
                'last_login_time': last_login_time,
                'subscription_plan': subscription_info,
            })
        return api_response(
            message="User details fetched successfully",
            message_type="success",
            status_code=status.HTTP_200_OK,
            data=user_details_data
        )

# Action Buttons APIs for UserDetails
class EditUserAPIView(APIView):
    def put(self, request, pk, format=None):
        student = get_object_or_404(Student, pk=pk)
        data = request.data
        student.first_name = data.get('first_name', student.first_name)
        student.last_name = data.get('last_name', student.last_name)
        student.email = data.get('email', student.email)
        # student.phone_number = data.get('phone_number', student.phone_number)
        student.is_active = data.get('is_active', student.is_active)
        student.save()
        if "phone_number" in request.data and request.data["phone_number"] != student.phone_number:
            new_phone = request.data["phone_number"]
 
            if Student.objects.filter(phone_number=new_phone).exists():
                return api_response(
                    message="Phone number already in use.",
                    message_type="error",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
 
            # Do NOT update yet — just trigger OTP
            responce = send_otp_newphone_number(student, 'OTP For Phone number change', new_phone)
 
            # student.save()
 
            # return api_response(
            #                     message="For Change Phone Number on School Book an OTP sent to your New Phone Number.",
            #                     message_type="success",
            #                     status_code=status.HTTP_200_OK
            #                 )
            return responce




        updated_student_data = {
            'id': student.pk,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'email': student.email,
            'phone_number': student.phone_number,
            'is_active': student.is_active
        }
        return api_response(
            message="User updated successfully",
            message_type="success",
            status_code=status.HTTP_200_OK,
            data=updated_student_data
        )

class SuspendUserAPIView(APIView):
    def post(self, request, pk, format=None):
        is_active = request.data.get("is_active", False)
        student = get_object_or_404(Student, pk=pk)



        # if student.is_active == False:
        #     student.is_active = True
        # elif student.is_active == True:
        #     student.is_active = False

        student.is_active = is_active
        

        student.save()
        suspended_student_data = {
            'id': student.pk,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'email': student.email,
            'is_active': student.is_active
        }
        if student.is_active == False:
            return api_response(
                message="User suspended successfully",
                message_type="success",
                status_code=status.HTTP_200_OK,
                data=suspended_student_data
            )
        elif student.is_active == True:
            return api_response(
                message="User Activated successfully",
                message_type="success",
                status_code=status.HTTP_200_OK,
                data=suspended_student_data
            )

class DeleteUserAPIView(APIView):
    def delete(self, request, pk, format=None):
        student = get_object_or_404(Student, pk=pk)
        deleted_student_data = {
            'id': student.pk,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'email': student.email,
        }
        student.delete()
        return api_response(
            message="User deleted successfully",
            message_type="success",
            status_code=status.HTTP_200_OK,
            data=deleted_student_data
        )

class ResetPasswordAPIView(APIView):
    def post(self, request, pk, format=None):
        student = get_object_or_404(Student, pk=pk)
        new_password = request.data.get('new_password')
        student.set_password(new_password)
        student.save()
        reset_password_student_data = {
            'id': student.pk,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'email': student.email
        }
        return api_response(
            message="Password reset successfully. A new password has been sent to the user.",
            message_type="success",
            status_code=status.HTTP_200_OK,
            data=reset_password_student_data
        )
    

# Assuming a simple in-memory storage for OTPs for this example. 
# In a real app, you would use a database or cache (like Redis) for this.



# class SendOTPAPIView(APIView):
#     def post(self, request, format=None):
#         phone_number = request.data.get('phone_number')

#         if not phone_number:
#             return api_response(
#                 "Phone number is required.",
#                 "error",
#                 status.HTTP_400_BAD_REQUEST
#             )
        
#         # Generate a 6-digit OTP
#         otp = str(random.randint(100000, 999999))
        
#         # Store the OTP in our temporary storage

        
#         # --- Placeholder for sending SMS ---
#         # In a real application, you would integrate with an SMS service here.
#         # Example using a print statement for testing:
#         print(f"Sending OTP {otp} to phone number {phone_number}")

#         return api_response(
#             "OTP sent successfully.",
#             "success",
#             status.HTTP_200_OK
#         )
    

# In your studentbookadminfrontend/views/userdetails_views.py file

class VerifyAndUpdatePhoneAPIView(APIView):
    def post(self, request, pk, format=None):
        phone_number = request.data.get('phone_number')
        otp_received = request.data.get('otp')
        
        student = get_object_or_404(Student, pk=pk)
        
        # Check if the phone number and OTP are provided
        if not phone_number or not otp_received:
            return api_response(
                "Phone number and OTP are required.",
                "error",
                status.HTTP_400_BAD_REQUEST
            )

        # Retrieve the OTP from our temporary storage

        if otp_received == student.otp:
            # If the OTP is correct, update the student's phone number
            student.phone_number = phone_number
            student.save()
            
            # Optional: Delete the OTP from storage to prevent reuse

                
            updated_student_data = {
                'id': student.pk,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'phone_number': student.phone_number,
                'is_active': student.is_active
            }

            return api_response(
                message= "Phone number updated successfully.",
                message_type="success",
                status_code=status.HTTP_200_OK,
                data=updated_student_data
            )
        else:
             # ❌ OTP didn’t match
            return api_response(
               message= "In Correct Otp.",
               message_type= "error",
               status_code= status.HTTP_400_BAD_REQUEST
        
            )




