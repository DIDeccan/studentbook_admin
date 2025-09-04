# views.py

from rest_framework import generics, status
from studentbookadminfrontend.models import Class
from studentbookadminfrontend.serializers.dashboard_serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from studentbookadminfrontend.models import Student
from django.db.models import Count
from rest_framework.response import Response
from studentbookadminfrontend.serializers.dashboard_serializers import StudentSerializer
from django.db.models import F
from django.http import JsonResponse
from ..models import SubscriptionOrder
from studentbookadminfrontend.models import User
from studentbookadminfrontend.serializers.dashboard_serializers import UserLoginSerializer




# Custom response wrapper

def api_response(message, message_type, status_code, data=None):

    return Response(
        {

            "message": message,
            "message_type": message_type,
            "status_code": status_code,
            "data": data,
        }

    )
 
class ClassListAPIView(APIView):

    def get(self, request):
        # Get all class objects
        queryset = Class.objects.all()
        # Serialize the queryset
        serializer = ClassSerializer(queryset, many=True)
        # Return response
        return Response(
            {
                "message": "Class data fetched successfully",
                "message_type": "success",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    
class StudentListAPIView(APIView):

    def get(self, request):
        # Get all students
        queryset = Student.objects.all()
        
        # Serialize queryset
        serializer = StudentSerializer(queryset, many=True)

        # Return API response
        return Response(
            {
                "message": "Student data fetched successfully",
                "message_type": "success",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

class ClassDistributionAPIView(APIView):

    def get(self, request):
        # Aggregate students by class
        class_counts = Student.objects.values('student_class').annotate(count=Count('id'))

        # Prepare data for pie chart
        chart_data = [
            {"class": Class.objects.get(id = item['student_class']).name, "number_of_student": item['count']}
            for item in class_counts
        ]

        return api_response(
        
                message= "Class-wise distribution fetched successfully",
                message_type= "success",
                status_code=status.HTTP_200_OK,
                data= chart_data
            
        )

# class TransactionsAPIView(APIView):

#     def get(self,request):

#         transactions = SubscriptionOrder.objects.all().order_by('-id')[:5]
#         # Mapping payment modes to readable text
#         payment_modes = {
#             'upi': 'UPI',
#             'credit_card': 'Credit Card',
#             'debit_card': 'Debit Card',
#             'bank': 'Bank Account'
#         }
#         print("transactions",transactions)

#         data = [
#         {
#             "transaction_id": o.id,
#             "student": o.student.phone_number,
#             "course": o.course.name,
#             "status": o.payment_status,
#             "amount": o.price,
#             "date": o.created_at, 
#         }
#         for o in transactions
#     ]
   


#         return api_response(
        
#                 message= "Class-wise distribution fetched successfully",
#                 message_type= "success",
#                 status_code=status.HTTP_200_OK,
#                 data = data
                
#         )


class TransactionsAPIView(APIView):

    def get(self, request):

        transactions = SubscriptionOrder.objects.all().order_by('-id')

        # Apply quick filter (status=completed/failed/pending)
        status_filter = request.query_params.get('status')
        if status_filter:
            transactions = transactions.filter(payment_status=status_filter)

        transactions = transactions[:5]

        data = [
            {
                "transaction_id": o.transaction_id,
                "user_name": f"{o.student.first_name} {o.student.last_name}",
                "user_email": o.student.email,
                "student_phone": o.student.phone_number,
                "class_name": o.course.name,  
                "status": o.payment_status,
                "amount": o.price,
                "date": o.created_at,
                "payment_mode":o.payment_mode
            }
            for o in transactions
        ]

        return api_response(
            message="Last 5 transactions fetched successfully",
            message_type="success",
            status_code=status.HTTP_200_OK,
            data=data
        )



class UserLoginListAPIView(APIView):
    def get(self, request):
        # Fetch all users (or add filters later)
        queryset = User.objects.all().order_by('-login_time')
        print(queryset.count())

        # Serialize data
        serializer = UserLoginSerializer(queryset, many=True)

        return api_response(
            message="User login details fetched successfully",
            message_type="success",
            status_code=status.HTTP_200_OK,
            data=serializer.data
        )

 