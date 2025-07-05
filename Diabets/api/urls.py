from django.urls import path
from diabetic.views import (
    admin_login_view,
    login_view,
    doctor_login_view,
    patient_login_view,
    manage_user,
    manage_patient,
    manage_doctor,
    manage_sugar,
    manage_comment,
    manage_educational,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # path('admin/', admin_login_view, name='admin_login'),
    path('doctor-login/', doctor_login_view, name='doctor_login'),
    path('patient-login/', patient_login_view, name='patient_login'),
    # This is the login endpoint for the admin user, which is now handled by the custom

    path('admin-login/', login_view, name='admin_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('user/', manage_user),
    path('user/<int:id>/', manage_user),

    path('patient/', manage_patient),
    path('patient/<int:id>/', manage_patient),

    path('doctor/', manage_doctor),
    path('doctor/<int:id>/', manage_doctor),

    path('sugar/', manage_sugar),
    path('sugar/<int:id>/', manage_sugar),

    path('comment/', manage_comment),
    path('comment/<int:id>/', manage_comment),

    path('educational-content/', manage_educational),
    path('educational-content/<int:id>/', manage_educational),
]
