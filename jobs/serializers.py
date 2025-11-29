from rest_framework import serializers
from .models import Job, Category, Application

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
class JobSerializer(serializers.ModelSerializer):
    """
    Standard Job Serializer for listing and creating jobs.
    """
    # Read-only fields to show names instead of just IDs
    employer_name = serializers.ReadOnlyField(source='employer.first_name')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Job
        fields = (
            'id', 'employer', 'employer_name', 'category', 'category_name',
            'title', 'description', 'location', 'salary', 'job_type', 
            'company_logo', 'created_at', 'is_active'
        )
        # Important: 'employer' is read-only so users cannot fake it
        read_only_fields = ('employer', 'created_at')

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('id', 'job', 'applicant', 'resume', 'cover_letter', 'status', 'applied_at')
        read_only_fields = ('applicant', 'status', 'applied_at')