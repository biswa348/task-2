from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=64, unique=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    location = models.CharField(max_length=64, blank=True, null=True)
    manager = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=128)
    level = models.IntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='roles')
    responsibilities = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.department.name})"

class Employee(models.Model):
    GENDER_CHOICES = [('Male','Male'), ('Female','Female'), ('Other','Other')]

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='employees')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='employees')
    gender = models.CharField(max_length=16, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_joining = models.DateField(blank=True, null=True)
    salary = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    location = models.CharField(max_length=128, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=16, choices=[('Present','Present'),('Absent','Absent'),('Leave','Leave')], default='Present')
    check_in = models.TimeField(blank=True, null=True)
    check_out = models.TimeField(blank=True, null=True)
    hours = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        unique_together = ('employee', 'date')

    def __str__(self):
        return f"{self.employee} - {self.date} - {self.status}"

class Performance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='performances')
    review_date = models.DateField()
    reviewer = models.CharField(max_length=128)
    score = models.DecimalField(max_digits=4, decimal_places=2)  # e.g., 4.25 / 5.00
    goals_met = models.IntegerField(default=0)
    strengths = models.TextField(blank=True, null=True)
    weaknesses = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-review_date']

    def __str__(self):
        return f"{self.employee} - {self.review_date} - {self.score}"
