import random
from datetime import date, timedelta
from faker import Faker
fake = Faker()

from employees.models import Department, Role, Employee, Attendance, Performance

Attendance.objects.all().delete()
Performance.objects.all().delete()
Employee.objects.all().delete()
Role.objects.all().delete()
Department.objects.all().delete()

dept_names = ["IT", "HR", "Finance", "Marketing"]
depts = []
for name in dept_names:
    d = Department.objects.create(name=name, code=name[:3].upper())
    depts.append(d)

roles_map = {
    "IT": ["Software Engineer", "Senior Engineer", "Tech Lead"],
    "HR": ["Recruiter", "HR Manager"],
    "Finance": ["Accountant", "Finance Manager"],
    "Marketing": ["SEO Specialist", "Marketing Manager"],
}

for dept in depts:
    for r in roles_map.get(dept.name, []):
        Role.objects.create(name=r, department=dept)

employees = []
for i in range(5):
    dept = random.choice(depts)
    role = Role.objects.filter(department=dept).order_by('?').first()
    doj = date.today() - timedelta(days=random.randint(100, 2000))
    emp = Employee.objects.create(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.unique.email(),
        phone=fake.phone_number(),
        department=dept,
        role=role,
        gender=random.choice(["Male", "Female", "Other"]),
        date_of_joining=doj,
        salary=round(random.uniform(30000, 120000), 2),
        experience_years=random.randint(1, 20),
        location=fake.city()
    )
    employees.append(emp)
    for d_offset in range(7):
        day = date.today() - timedelta(days=d_offset)
        status = random.choices(["Present","Absent","Leave"], weights=(80,10,10))[0]
        Attendance.objects.create(employee=emp, date=day, status=status)
    for k in range(2):
        Performance.objects.create(
            employee=emp,
            review_date=date.today() - timedelta(days=30*(k+1)),
            reviewer=fake.name(),
            score=round(random.uniform(2.5,5.0), 2),
            goals_met=random.randint(0,10),
            strengths="Good at collaboration",
            weaknesses="Needs time management"
        )

print("Created", Employee.objects.count(), "employees with attendance and performance records")
