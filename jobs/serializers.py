from rest_framework import serializers
from .models import Job, Category, Application
from users.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    """
    Standard Job Serializer for listing jobs.
    """
    employer_name = serializers.ReadOnlyField(source='employer.first_name')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Job
        fields = (
            'id', 'employer', 'employer_name', 'category', 'category_name',
            'title', 'description', 'location', 'salary', 'job_type', 
            'company_logo', 'created_at', 'is_active'
        )
        read_only_fields = ('employer', 'created_at')

    def create(self, validated_data):
        # Automatically assign the logged-in user as the employer
        user = self.context['request'].user
        return Job.objects.create(employer=user, **validated_data)

class ApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer for submitting applications.
    """
    class Meta:
        model = Application
        fields = ('id', 'job', 'applicant', 'resume', 'cover_letter', 'status', 'applied_at')
        read_only_fields = ('applicant', 'status', 'applied_at')

    def create(self, validated_data):
        user = self.context['request'].user
        # Ensure user hasn't already applied (handled by unique_together in Model)
        return Application.objects.create(applicant=user, **validated_data)