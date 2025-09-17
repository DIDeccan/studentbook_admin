from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView 
from studentbookadminfrontend.views.dashboard_views import api_response
from studentbookadminfrontend.serializers.content_management_serializer import *




class ClassWIthSubjectsView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        classes = Class.objects.all().order_by('id')
        data = []
        for cls in classes:
            subjects = Subject.objects.filter(course=cls.id).order_by('id')
            subject_data = []
            for subject in subjects:
                subject_data.append({
                    'subject_id': subject.id,
                    'subject_name': subject.name,
                    # 'subject_image': subject.image.url if subject.image else None
                })
            # subject_serializer = SubjectSerializer(subjects, many=True)
 
            class_data = {
                'class_id': cls.id,
                'class_name': cls.name,
                'subjects': subject_data
            }
            data.append(class_data)
       
        return api_response(
            message="Classes with subjects fetched successfully",
            message_type="success",
            status_code=status.HTTP_200_OK,
            data=data
        )
 
