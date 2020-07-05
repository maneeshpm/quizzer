from django.urls import path
from userAccounts.api.views import(
	UserCreateAPIView,
    UserLoginAPIView
    )

app_name = 'userAccounts'


urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
]
