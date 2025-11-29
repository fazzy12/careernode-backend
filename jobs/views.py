from rest_framework import generics, permissions, filters
from django_filters import rest_framework as django_filters
from .models import Job, Category
from .serializers import JobSerializer, CategorySerializer
from .permissions import IsEmployerOrReadOnly, IsOwnerOrReadOnly


# --- Custom Filter ---
class JobFilter(django_filters.FilterSet):
    # Use 'icontains' (case-insensitive partial match) for location & title
    location = django_filters.CharFilter(lookup_expr='icontains')
    title = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Job
        fields = ['category', 'job_type', 'location', 'title']
        

# --- Views ---

class CategoryListView(generics.ListAPIView):
    """
    GET /api/categories/
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)


class JobListCreateView(generics.ListCreateAPIView):
    """
    GET /api/jobs/ - Public List with filters
    POST /api/jobs/ - Create (Employer Only)
    """
    # Show active jobs, ordered by newest first
    queryset = Job.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = JobSerializer
    permission_classes = (IsEmployerOrReadOnly,)

    # Configure Filtering
    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = JobFilter
    search_fields = ['title', 'description', 'location'] # For ?search= parameter

    def perform_create(self, serializer):
        # Automatically set the 'employer' to the logged-in user
        serializer.save(employer=self.request.user)


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/jobs/{id}/ - Retrieve (Public)
    PATCH /api/jobs/{id}/ - Update (Owner/Admin Only)
    DELETE /api/jobs/{id}/ - Delete (Owner/Admin Only)
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (IsOwnerOrReadOnly,)