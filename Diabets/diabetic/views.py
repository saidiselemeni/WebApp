from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    UserSerializer,
    PatientSerializer,
    DoctorSerializer,
    SugarTestSerializer,
    CommentSerializer,
    EducationalContentSerializer,
)
from .models import User, Patient, Doctor, SugarTest, Comment, EducationalContent

# Generic API Function with superuser permission
# from rest_framework.decorators import api_view, permission_classes

def gain_api(model_class, serializer_class):
    @api_view(['GET', 'POST', 'PUT', 'DELETE'])
    # @permission_classes([IsAuthenticated])  # Only authentication required, not superuser
    def api(request, id=None):
   
        if request.method == 'GET':
            if id:
                try:
                    instance = model_class.objects.get(id=id)
                    serializer = serializer_class(instance)
                    return Response(serializer.data)
                except model_class.DoesNotExist:
                    return Response({'message': 'Object not found'}, status=404)
            else:
                instances = model_class.objects.all()
                serializer = serializer_class(instances, many=True)
                return Response(serializer.data)

        elif request.method == 'POST':
            serializer = serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)

        elif request.method == 'PUT':
            if id:
                try:
                    instance = model_class.objects.get(id=id)
                    serializer = serializer_class(instance, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                    return Response(serializer.errors, status=400)
                except model_class.DoesNotExist:
                    return Response({'message': 'Object not found'}, status=404)
            return Response({'message': 'ID is required for update'}, status=400)

        elif request.method == 'DELETE':
            if id:
                try:
                    instance = model_class.objects.get(id=id)
                    instance.delete()
                    return Response({'message': 'Deleted successfully'}, status=200)
                except model_class.DoesNotExist:
                    return Response({'message': 'Object not found'}, status=404)
            return Response({'message': 'ID is required for deletion'}, status=400)

        return Response({'message': 'Invalid method'}, status=405)

    return api


@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'detail': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=email, password=password)  # username=email here

    if user is None:
        return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': {
            'id': user.id,
            'email': user.email,
            'role': user.role,
            # add other fields you want to expose
        },
    })


@api_view(['POST'])
def admin_login_view(request):
    return Response({"message": "Admin login endpoint"})




# API endpoints with superuser restriction
manage_user = gain_api(User, UserSerializer)
manage_patient = gain_api(Patient, PatientSerializer)
manage_doctor = gain_api(Doctor, DoctorSerializer)
manage_sugar = gain_api(SugarTest, SugarTestSerializer)
manage_comment = gain_api(Comment, CommentSerializer)
manage_educational = gain_api(EducationalContent, EducationalContentSerializer)



# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import DoctorLoginSerializer

@api_view(['POST'])
def doctor_login_view(request):
    serializer = DoctorLoginSerializer(data=request.data)
    if serializer.is_valid():
        doctor = serializer.validated_data['doctor']
        return Response({
            "doctor": {
            "id": 1,
            "email": "bitam11-006@suza.ac.tz",
            "role": "Patient"
        }

        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def patient_login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'detail': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        patient = Patient.objects.get(email=email, password=password)
    except Patient.DoesNotExist:
        return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({
        'patient': {
                'id': patient.id,
                'email': patient.email,
                'role': 'Patient',  # or patient.role if exists
                # add other fields as needed, e.g. patient_name
            }
    })