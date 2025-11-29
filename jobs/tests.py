import tempfile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from .models import Job, Category

User = get_user_model()

class JobEndpointTests(APITestCase):
    def setUp(self):
        # --- 1. Users Setup ---
        self.employer = User.objects.create_user(
            email='employer@test.com', password='password123', role='employer'
        )
        self.other_employer = User.objects.create_user(
            email='other@test.com', password='password123', role='employer'
        )
        self.applicant = User.objects.create_user(
            email='applicant@test.com', password='password123', role='applicant'
        )
        self.admin = User.objects.create_superuser(
            email='admin@test.com', password='password123'
        )

        # --- 2. Data Setup ---
        self.category_tech = Category.objects.create(name='Technology', slug='tech')
        self.category_marketing = Category.objects.create(name='Marketing', slug='marketing')

        # Create a dummy image for testing uploads
        image = Image.new('RGB', (100, 100))
        self.tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(self.tmp_file)
        self.tmp_file.seek(0)
        self.test_image = SimpleUploadedFile("logo.jpg", self.tmp_file.read(), content_type="image/jpeg")

        # Create an initial Job (Owned by self.employer)
        self.job = Job.objects.create(
            employer=self.employer,
            category=self.category_tech,
            title='Senior Python Developer',
            description='We need a Django expert.',
            location='New York, NY',
            salary=150000,
            job_type='FT',
            is_active=True
        )

        # Define URLs
        self.list_url = reverse('job_list_create')       # /api/jobs/
        self.detail_url = reverse('job_detail', args=[self.job.id]) # /api/jobs/{id}/

    def tearDown(self):
        # Clean up temporary files
        self.tmp_file.close()

    # ----------------------------------------------------------------
    # 1. GET /api/jobs/ (List & Filter) - PUBLIC
    # ----------------------------------------------------------------
    def test_public_can_list_jobs(self):
        """Anyone should be able to see the list of jobs."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Senior Python Developer')

    def test_filter_jobs_by_search(self):
        """Test ?search= query parameter."""
        # Create a second job that shouldn't match
        Job.objects.create(
            employer=self.employer, category=self.category_marketing,
            title='Marketing Manager', location='Boston', job_type='FT'
        )
        
        # Search for "Python"
        response = self.client.get(f"{self.list_url}?search=Python")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Senior Python Developer')

    def test_filter_jobs_by_location(self):
        """Test ?location= query parameter."""
        # Search for "New York"
        response = self.client.get(f"{self.list_url}?location=New York")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Search for "London" (Should be empty)
        response = self.client.get(f"{self.list_url}?location=London")
        self.assertEqual(len(response.data), 0)

    # ----------------------------------------------------------------
    # 2. POST /api/jobs/ (Create) - EMPLOYER ONLY
    # ----------------------------------------------------------------
    def test_employer_can_create_job(self):
        """Employers should be able to create jobs."""
        self.client.force_authenticate(user=self.employer)
        data = {
            "title": "Junior Dev",
            "description": "Learning opportunity",
            "category": self.category_tech.id,
            "location": "Remote",
            "salary": 60000,
            "job_type": "FT",
            "company_logo": self.test_image  # Test image upload
        }
        response = self.client.post(self.list_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Job.objects.count(), 2)
        self.assertEqual(Job.objects.last().employer, self.employer)

    def test_applicant_cannot_create_job(self):
        """Applicants should get 403 Forbidden."""
        self.client.force_authenticate(user=self.applicant)
        data = {"title": "Hacker Job", "description": "test", "category": self.category_tech.id}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_create_job(self):
        """Guests should get 401 Unauthorized."""
        data = {"title": "Ghost Job"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ----------------------------------------------------------------
    # 3. GET /api/jobs/{id}/ (Retrieve) - PUBLIC
    # ----------------------------------------------------------------
    def test_retrieve_single_job(self):
        """Anyone can view a specific job detail."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Senior Python Developer')

    # ----------------------------------------------------------------
    # 4. PATCH /api/jobs/{id}/ (Update) - JOB OWNER ONLY
    # ----------------------------------------------------------------
    def test_owner_can_update_job(self):
        """The employer who created the job can edit it."""
        self.client.force_authenticate(user=self.employer)
        data = {"salary": 160000, "title": "Lead Python Developer"}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.job.refresh_from_db()
        self.assertEqual(self.job.salary, 160000)
        self.assertEqual(self.job.title, "Lead Python Developer")

    def test_other_employer_cannot_update_job(self):
        """Employer B cannot edit Employer A's job."""
        self.client.force_authenticate(user=self.other_employer)
        data = {"salary": 200000}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ----------------------------------------------------------------
    # 5. DELETE /api/jobs/{id}/ - JOB OWNER OR ADMIN
    # ----------------------------------------------------------------
    def test_owner_can_delete_job(self):
        """The owner should be able to delete the job."""
        self.client.force_authenticate(user=self.employer)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Job.objects.count(), 0)

    def test_admin_can_delete_job(self):
        """Admins should be able to force delete any job."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Job.objects.count(), 0)

    def test_applicant_cannot_delete_job(self):
        """Applicants cannot delete jobs."""
        self.client.force_authenticate(user=self.applicant)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
