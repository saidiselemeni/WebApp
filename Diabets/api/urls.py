from django.urls import path ,include
from django.conf import settings
# from myapp.views import api_view
from diabetic . views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # For logging in
    TokenRefreshView,     # For refreshing the JWT token
)


urlpatterns = [
    path('login/', custom_login_view, name='custom_login'), # Obtain JWT token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh JWT token
    
    # User-related URL
    #path('users/me/',views.curent_user , name='current_user'),
    path('patient/', manage_patient ),
    path('patient/<int:id>/', manage_patient ),
    path('my-tests/', get_my_tests),
    path('sugar/', manage_sugar),
    path('sugar/<int:id>/', manage_sugar ),
    path('doctor-login/', doctor_login, name='doctor-login'),
    path('comment/', manage_comment),
    path('comment/<int:id>/', manage_comment ),
    path('educational-content/',manage_Educational ),
    path('educational-content/<int:id>/',manage_Educational ),
    path('doctor/', manage_doctor),
    path('doctor/<int:id>/', manage_doctor ),
    
]