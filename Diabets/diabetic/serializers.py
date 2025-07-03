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