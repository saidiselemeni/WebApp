# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import User, Patient, Doctor, SugarTest, Comment
from .serializers import UserSerializer, PatientSerializer, DoctorSerializer, SugarTestSerializer, CommentSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets
import json
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Doctor
from django.conf import settings
import jwt
import datetime
from rest_framework import generics
from .models import EducationalContent
from .serializers import EducationalContentSerializer


# Generic API Function

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status

class EducationalContentUploadView(generics.ListCreateAPIView):
    queryset = EducationalContent.objects.all()
    serializer_class = EducationalContentSerializer

def gain_api(model_class, serializer_class):
    @api_view(['GET', 'POST', 'PUT', 'DELETE'])
    
    def api(request, id=None):
        # For GET
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
        
        # For Insert
        elif request.method == 'POST':
            serializer = serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)

        # For Update
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
                    return JsonResponse({'message': 'Object not found'}, status=404)
            return Response({'message': 'ID is required for update'}, status=400)

        # For Delete
        elif request.method == 'DELETE':
            if id:
                try:
                    instance = model_class.objects.get(id=id)
                    instance.delete()
                    return Response({'message': 'Deleted successfully'}, status=204)
                except model_class.DoesNotExist:
                    return JsonResponse({'message': 'Object not found'}, status=404)
            return Response({'message': 'ID is required for deletion'}, status=400)

        return JsonResponse({'message': 'Invalid method'}, status=405)

    return api



def generate_token_for_doctor(doctor):
    payload = {
        'doctor_id': doctor.id,
        'email': doctor.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import SugarTest
from .serializers import SugarTestSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_tests(request):
    user = request.user
    if hasattr(user, 'patient'):
        patient = user.patient
        tests = SugarTest.objects.filter(patient=patient).order_by('-test_date')
        serializer = SugarTestSerializer(tests, many=True)
        return Response(serializer.data)
    return Response({"detail": "Not a patient user."}, status=400)

@api_view(['POST'])
def custom_login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'detail': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        doctor = Doctor.objects.get(email=email)

        # NOTE: Using plain password comparison — not secure for production!
        if doctor.password != password:
            return Response({'detail': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)

        token = generate_token_for_doctor(doctor)

        return Response({
            'access': token,
            'doctor_id': doctor.id,
            'doctor_name': doctor.doctor_name,
            'email': doctor.email,
        })

    except Doctor.DoesNotExist:
        return Response({'detail': 'Doctor not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def doctor_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        doctor = Doctor.objects.get(email=email, password=password)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)
    except Doctor.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# API Endpoints
manage_user = gain_api(User, UserSerializer)
manage_patient = gain_api(Patient, PatientSerializer)
manage_doctor = gain_api(Doctor, DoctorSerializer)
manage_sugar = gain_api(SugarTest, SugarTestSerializer)
manage_comment = gain_api(Comment, CommentSerializer)
manage_Educational = gain_api(EducationalContent, EducationalContentSerializer)
