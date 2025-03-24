from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
User = get_user_model()
from django.contrib.auth.models import Group
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


    
    def perform_create(self, serializer):
        user = serializer.save()

        # Ensure the "Drivers" group exists and add the user to it
        drivers_group, created = Group.objects.get_or_create(name="Drivers")
        user.groups.add(drivers_group)
        user.save()

class LoginView(TokenObtainPairView):
    pass