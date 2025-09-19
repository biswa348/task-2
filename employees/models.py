from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="roles")

    def __str__(self):
        return f"{self.name} ({self.department.name})"

class Employee(models.Model):
    GENDER_CHOICES = (("Male","Male"),("Female","Female"),("Other","Other"))
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="employees")
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name="employees")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_joining = models.DateField(blank=True, null=True)
    salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    experience_years = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Attendance(models.Model):
    STATUS_CHOICES = (("Present","Present"),("Absent","Absent"),("Leave","Leave"))
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendance")
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ("employee", "date")

class Performance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="performances")
    review_date = models.DateField()
    reviewer = models.CharField(max_length=150)
    score = models.DecimalField(max_digits=4, decimal_places=2)
    goals_met = models.IntegerField(default=0)
    strengths = models.TextField(blank=True, null=True)
    weaknesses = models.TextField(blank=True, null=True)
