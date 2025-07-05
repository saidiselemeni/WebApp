from rest_framework import serializers
from .models import User, Patient, Doctor, SugarTest, Comment, EducationalContent

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'


class SugarTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SugarTest
        fields = '__all__'




class CommentSerializer(serializers.ModelSerializer):
    sugartest = serializers.PrimaryKeyRelatedField(queryset=SugarTest.objects.all())
    
    class Meta:
        model = Comment
        fields = '__all__'

class EducationalContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalContent
        fields = '__all__'


# serializers.py
from rest_framework import serializers
from .models import Doctor

class DoctorLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        doctor = Doctor.objects.filter(email=email, password=password).first()
        if not doctor:
            raise serializers.ValidationError("Invalid email or password.")

        data['doctor'] = doctor
        return data
class PatientLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        patient = Patient.objects.filter(email=email, password=password).first()
        if not patient:
            raise serializers.ValidationError("Invalid email or password.")

        data['patient'] = patient
        return data