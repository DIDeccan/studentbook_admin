from rest_framework import serializers
from studentbookadminfrontend.models import Student
from studentbookadminfrontend.models import Class  # make sure you have a Class model
from studentbookadminfrontend.models import User


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id','last_login','email','first_name','last_name','phone_number','otp','user_type','registered_date','student_class']  # or list the fields you want

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'name','amount']  # or list the fields you want

# class UserLoginSerializer(serializers.ModelSerializer):
#     name = serializers.SerializerMethodField()
#     status = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = ['id', 'name', 'email', 'phone_number', 'login_time', 'status']

#     def get_name(self, obj):
#         return f"{obj.first_name} {obj.last_name}"

#     def get_status(self, obj):
#         return "Active" if obj.is_active else "Inactive"
    





