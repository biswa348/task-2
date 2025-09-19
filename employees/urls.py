from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmployeeViewSet,
    by_department,
    avg_salary_by_department,
    gender_split,
    experience_histogram,
    visualizer,
)

router = DefaultRouter()
router.register("employees", EmployeeViewSet, basename="employee")

app_name = "employees"

urlpatterns = [
    path("", include(router.urls)),
    path("analytics/by-department/", by_department, name="by-department"),
    path("analytics/avg-salary-by-department/", avg_salary_by_department, name="avg-salary-by-department"),
    path("analytics/gender-split/", gender_split, name="gender-split"),
    path("analytics/experience-histogram/", experience_histogram, name="experience-histogram"),
    path("visualizer/", visualizer, name="visualizer"),
]
