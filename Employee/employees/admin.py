from django.contrib import admin
from .models import Employee
# Register your models here.

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name','email','department','role','salary')
    search_fields = ('first_name','last_name','email','department','role')
