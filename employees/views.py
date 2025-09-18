from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.db.models import Count, Avg
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import F

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'per_page'
    max_page_size = 1000

class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Return paginated list of employees. Filtering by department and gender using query params.
    """
    queryset = Employee.objects.all().order_by('id')
    serializer_class = EmployeeSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = super().get_queryset()
        dept = self.request.query_params.get('department')
        gender = self.request.query_params.get('gender')
        if dept:
            qs = qs.filter(department__iexact=dept)
        if gender:
            qs = qs.filter(gender__iexact=gender)
        return qs

# Analytics endpoints (function-based)
@api_view(['GET'])
def by_department(request):
    q = Employee.objects.values('department').annotate(count=Count('id')).order_by('-count')
    return Response({item['department'] or 'Unknown': item['count'] for item in q})

@api_view(['GET'])
def avg_salary_by_department(request):
    q = Employee.objects.values('department').annotate(avg_salary=Avg('salary'))
    # convert Decimal to float
    return Response({item['department'] or 'Unknown': float(item['avg_salary']) if item['avg_salary'] is not None else None for item in q})

@api_view(['GET'])
def gender_split(request):
    q = Employee.objects.values('gender').annotate(count=Count('id'))
    return Response({item['gender'] or 'Unknown': item['count'] for item in q})

@api_view(['GET'])
def experience_histogram(request):
    bins = int(request.query_params.get('bins', 5))
    vals = list(Employee.objects.exclude(experience_years__isnull=True).values_list('experience_years', flat=True))
    vals = [float(v) for v in vals]
    if not vals:
        return Response({})
    mn, mx = min(vals), max(vals)
    if mn == mx:
        return Response({f"{mn}": len(vals)})
    width = (mx - mn) / bins
    buckets = {}
    for i in range(bins):
        low = mn + i * width
        high = low + width
        label = f"{round(low,1)}-{round(high,1)}"
        buckets[label] = 0
    for v in vals:
        idx = int((v - mn) / width)
        if idx == bins:
            idx = bins - 1
        low = mn + idx * width
        high = low + width
        label = f"{round(low,1)}-{round(high,1)}"
        buckets[label] += 1
    return Response(buckets)
