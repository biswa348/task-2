from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, by_department, avg_salary_by_department, gender_split, experience_histogram

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/by-department/', by_department, name='by-department'),
    path('analytics/salary-by-department/', avg_salary_by_department, name='salary-by-dept'),
    path('analytics/gender-split/', gender_split, name='gender-split'),
    path('analytics/experience-histogram/', experience_histogram, name='experience-histogram'),
]
