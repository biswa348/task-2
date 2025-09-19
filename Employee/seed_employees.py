import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Employee.settings")
django.setup()

from employees.models import Department, Role, Employee, Attendance, Performance
from faker import Faker
import random
from datetime import date, timedelta

fake = Faker()
Faker.seed(0)
random.seed(0)

DEPTS = ['Engineering','Sales','HR','Finance','Marketing']
ROLES = {
    'Engineering': ['Software Engineer','Senior Engineer','Tech Lead'],
    'Sales': ['Sales Executive','Account Manager'],
    'HR': ['Recruiter','HR Manager'],
    'Finance': ['Accountant','Finance Manager'],
    'Marketing': ['SEO','Marketing Manager'],
}

for d in DEPTS:
    dept, _ = Department.objects.get_or_create(name=d, defaults={'code': d[:3].upper()})
    for r in ROLES.get(d, []):
        Role.objects.get_or_create(name=r, department=dept)

employees = []
for i in range(5):
    dept = Department.objects.order_by('?').first()
    role = Role.objects.filter(department=dept).order_by('?').first()
    emp = Employee.objects.create(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.unique.email(),
        phone=fake.phone_number(),
        department=dept,
        role=role,
        gender=random.choice(['Male','Female','Other']),
        date_of_joining=date.today() - timedelta(days=random.randint(100,2000)),
        salary=round(random.uniform(30000,120000), 2),
        location=fake.city()
    )
    employees.append(emp)

    for d_offset in range(7):
        day = date.today() - timedelta(days=d_offset)
        status = random.choices(['Present','Absent','Leave'], weights=(80,10,10))[0]
        Attendance.objects.create(employee=emp, date=day, status=status)

    for k in range(2):
        Performance.objects.create(
            employee=emp,
            review_date=date.today()-timedelta(days=30*(k+1)),
            reviewer=fake.name(),
            score=round(random.uniform(2.5,5.0), 2),
            goals_met=random.randint(0,10),
            strengths='Good at collaboration',
            weaknesses='Needs time management'
        )

print("Created", len(employees), "employees with attendance and performance records")

