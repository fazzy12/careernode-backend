import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.files.base import ContentFile
from jobs.models import Category, Job, Application

User = get_user_model()

# Constants
NUM_EMPLOYERS = 10
NUM_APPLICANTS = 20
NUM_JOBS = 50
NUM_APPLICATIONS = 30

class Command(BaseCommand):
    help = 'Seeds the database with realistic test data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Seeding database...'))
        fake = Faker()

        self.stdout.write('Cleaning old data...')
        Application.objects.all().delete()
        Job.objects.all().delete()
        Category.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        self.stdout.write('Creating Categories...')
        categories_list = [
            'Software Development', 'Marketing', 'Design', 'Sales', 
            'Customer Support', 'Data Science', 'Product Management', 'Finance'
        ]
        categories = []
        for name in categories_list:
            cat, created = Category.objects.get_or_create(
                name=name, 
                defaults={'slug': slugify(name)}
            )
            categories.append(cat)

        self.stdout.write(f'Creating {NUM_EMPLOYERS} Employers...')
        employers = []
        for _ in range(NUM_EMPLOYERS):
            email = fake.unique.email()
            user = User.objects.create_user(
                email=email,
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role='employer'
            )
            employers.append(user)

        self.stdout.write(f'Creating {NUM_APPLICANTS} Applicants...')
        applicants = []
        for _ in range(NUM_APPLICANTS):
            email = fake.unique.email()
            user = User.objects.create_user(
                email=email,
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role='applicant'
            )
            applicants.append(user)

        self.stdout.write(f'Creating {NUM_JOBS} Jobs...')
        jobs = []
        job_types = ['FT', 'CT', 'RM']
        
        for _ in range(NUM_JOBS):
            employer = random.choice(employers)
            category = random.choice(categories)
            job = Job.objects.create(
                employer=employer,
                category=category,
                title=fake.job(),
                description=fake.text(max_nb_chars=500),
                location=fake.city(),
                salary=random.randint(40000, 150000),
                job_type=random.choice(job_types),
                is_active=True
            )
            jobs.append(job)

        self.stdout.write(f'Creating {NUM_APPLICATIONS} Applications...')
        
        dummy_resume = ContentFile(b"Dummy PDF content", name="resume.pdf")

        for _ in range(NUM_APPLICATIONS):
            applicant = random.choice(applicants)
            job = random.choice(jobs)
            
            if not Application.objects.filter(applicant=applicant, job=job).exists():
                Application.objects.create(
                    job=job,
                    applicant=applicant,
                    resume=dummy_resume,
                    cover_letter=fake.paragraph(),
                    status=random.choice(['pending', 'accepted', 'rejected'])
                )

        if not User.objects.filter(email='admin@careernode.com').exists():
            User.objects.create_superuser(
                'admin@careernode.com', 'password123', first_name='Admin', last_name='User'
            )
            self.stdout.write('Created Superuser: admin@careernode.com / password123')

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded database with {NUM_JOBS} jobs and {NUM_APPLICATIONS} applications!'))