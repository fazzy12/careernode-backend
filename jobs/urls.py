from django.urls import path
from .views import JobListCreateView, JobDetailView, CategoryListView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('jobs/', JobListCreateView.as_view(), name='job_list_create'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job_detail'),
]