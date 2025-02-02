from django.urls import path
from .views import RegisterView, LoginView , UpdateUserLocationView

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/update-location/', UpdateUserLocationView.as_view(), name='update-location'),
]
