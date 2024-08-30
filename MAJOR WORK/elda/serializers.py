from rest_framework import serializers
from .models import CustomUser, Staff, Candidate

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['full_name', 'email']

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['full_name', 'email', 'statement_of_purpose ', 'selected_university', 'selected_course']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'user_type']
