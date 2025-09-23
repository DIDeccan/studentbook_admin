from rest_framework_simplejwt.views import TokenObtainPairView
from studentbookadminfrontend.serializers.auth_serializers import CustomTokenObtainPairSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework import permissions
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from studentbookadminfrontend.views.content_management_views import api_response
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken





class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class LogoutView(APIView):
   
    permission_classes = [permissions.IsAuthenticated]
 
    def post(self, request):
       
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            # return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            return api_response(
                message="Refresh token is required.",
                message_type="error",
                status_code=status.HTTP_400_BAD_REQUEST
                        )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            user = request.user
            user.logout_time =  timezone.now() # Update logout time
            user.save(update_fields=["logout_time"])
 
            # return Response({"message": "Logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)
            return api_response(
                message="Logged out successfully.",
                message_type="success",
                status_code=status.HTTP_200_OK
                        )
 
        except TokenError:
            # return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
            return api_response(
                message="Invalid or expired token.",
                message_type="error",
                status_code=status.HTTP_400_BAD_REQUEST
                        )
 

class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]  # refresh usually doesn't require auth
 
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
 
            # If refresh token is invalid, let it fall to exception
            if response.status_code != status.HTTP_200_OK:
                return api_response(
                    message="Invalid or expired token.",
                    message_type="error",
                    status_code=response.status_code,
                )
 
            # On success
            return api_response(
                message="Token refreshed successfully",
                message_type="success",
                status_code=status.HTTP_200_OK,
                data=response.data
            )
 
        except (InvalidToken, TokenError):
            return api_response(
                message="Invalid or blacklisted token.",
                message_type="error",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
 