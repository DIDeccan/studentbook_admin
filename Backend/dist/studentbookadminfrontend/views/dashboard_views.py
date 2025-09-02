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




 