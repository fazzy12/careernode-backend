from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator

class Category(models.Model):
    """
    Schema:
    - id (Integer PK)
    - name (String)
    - slug (String, Unique)
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Job(models.Model):
    """
    Schema:
    - employer_id (FK User)
    - category_id (FK Category)
    - title (String)
    - description (Text)
    - company_logo (String/VARCHAR -> implemented as ImageField)
    - location (String)
    - salary (Decimal)
    - job_type (Enum)
    - created_at (DateTime)
    """
    JOB_TYPES = (
        ('FT', 'Full-time'),
        ('CT', 'Contract'),
        ('RM', 'Remote'),
    )

    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='posted_jobs'
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='jobs'
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    # Schema says String/VARCHAR, ImageField stores the string path in DB
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    location = models.CharField(max_length=100, db_index=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    job_type = models.CharField(max_length=2, choices=JOB_TYPES, default='FT')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.location}"

class Application(models.Model):
    """
    Schema:
    - job_id (FK Job)
    - applicant_id (FK User)
    - resume_url (String/File -> implemented as FileField)
    - cover_letter (Text)
    - status (Enum)
    - applied_at (DateTime)
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    job = models.ForeignKey(
        Job, 
        on_delete=models.CASCADE, 
        related_name='applications'
    )
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='my_applications'
    )
    
    # Stores the file path string in the DB (matching resume_url schema concept)
    resume = models.FileField(
        upload_to='resumes/%Y/%m/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx'])]
    )
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'applicant') # Ensures one application per job per user

    def __str__(self):
        return f"{self.applicant} -> {self.job.title}"