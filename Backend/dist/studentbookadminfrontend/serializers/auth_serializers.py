from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from studentbookadminfrontend.models import *
from rest_framework.exceptions import AuthenticationFailed,APIException
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings

class CustomAPIException(APIException):
    status_code = 400
 
    def __init__(self, message, message_type="error", data=None):
        if data is None:
            data = {}
            self.detail = {
                "message": message,
                "message_type": message_type,
            }
        else:
            self.detail = {
                "message": message,
                "message_type": message_type,
                "data": data
            }
 
 
 


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
 
        # Include user type in the token response
        token['user_type'] = user.user_type
 
        return token
 
    def validate(self, attrs):
       
 
        # data = super().validate(attrs)
        username = attrs.get("phone_number")
        password = attrs.get("password")
        # user = authenticate(request=self.context.get('request'), email=username, password=password)
        user = User.objects.filter(phone_number=username).first()

        print('user',user)
       
        if user is None:
            # raise AuthenticationFailed("Invalid credentials.")
            raise CustomAPIException(
                message= "User Not Found.",
                message_type= "error",
                data= None
            )
        user = authenticate(request=self.context.get('request'), phone_number=username, password=password)

        print("user",user)
       
        if user is None:
            # raise AuthenticationFailed("Invalid credentials.")
            raise CustomAPIException(
                message= "Invalid credentials.",
                message_type= "error",
                data= None
            )
        
        if not user.is_superuser:  # or user.user_type != "admin"
            raise CustomAPIException(
                message="You do not have admin access.",
                message_type="error",
                data=None
            )

 
 
        # Add custom claims
        data = super().validate(attrs)
        update_last_login(None, self.user)
        data['user_type'] = self.user.user_type
        data['is_active'] = self.user.is_active
        data['message_type'] = "success"
        return data
 
 
