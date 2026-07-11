from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/users/registration', views.RegistrationAPIView.as_view()),
    path('api/v1/users/login', views.AuthorizationAPIView.as_view()),
    path('api/v1/users/confirm/', views.ConfirmEmailAPIView.as_view()),
]