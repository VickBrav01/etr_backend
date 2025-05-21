from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()


class RegisterView(APIView):
    serializer_class = UserSerializer
    
    def post(self, request: Request, *args, **kwargs):
        data = self.request.data
        serializer = self.serializer_class(data=data)

        try:
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                response = {
                    "message": "User Created",
                    "data": serializer.data,
                }

                return Response(data=response, status=status.HTTP_201_CREATED)
            else:
                raise ValueError(serializer.errors)

        except Exception as e:
            response = {
                "message": "User Creation Failed",
                "error": str(e),
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    pass
