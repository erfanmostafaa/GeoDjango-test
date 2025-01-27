from rest_framework.generics import CreateAPIView ,GenericAPIView
from user.models import User 
from .serializers import CreateUserSerializer , LoginSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class =CreateUserSerializer


class LoginView(GenericAPIView):

    serializer_class = LoginSerializer

    def post (self , request , *args, **kwargs):
        serializer = self.get_serializer(Data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validata_data['user']


        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh" : str(refresh) , 
            "access" : str(refresh.access_token),
            "user" : {
                "id" : user.id , 
                "username" : user.username,
                "email" : user.email , 

            },
        } , status=status.HTTP_200_OK)