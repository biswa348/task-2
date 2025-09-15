from django.core.management.base import BaseCommand
from faker import Faker
import random
from datetime import date, timedelta
from employees.models import Employee
from django.db import IntegrityError

fake = Faker()
Faker.seed(0)
random.seed(0)

DEPARTMENTS = ["Engineering", "Sales", "HR", "Finance", "Marketing", "Support", "Operations"]
ROLES = {
    "Engineering": ["Software Engineer","Senior Engineer","Tech Lead","QA Engineer"],
    "Sales": ["Sales Executive","Account Manager","Sales Manager"],
    "HR": ["Recruiter","HR Manager"],
    "Finance": ["Accountant","Finance Manager"],
    "Marketing": ["SEO Specialist","Marketing Manager"],
    "Support": ["Support Engineer","Customer Support"],
    "Operations": ["Operations Executive","Ops Manager"]
}

def random_join_date(max_years=12):
    days = random.randint(0, 365 * max_years)
    return date.today() - timedelta(days=days)

class Command(BaseCommand):
    help = 'Generate synthetic employee records'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=100, help='Number of employees to create')

    def handle(self, *args, **options):
        count = options['count']
        created = 0
        for _ in range(count):
            dept = random.choice(DEPARTMENTS)
            role = random.choice(ROLES[dept])
            doj = random_join_date()
            exp_years = round((date.today() - doj).days / 365, 1)
            salary = round(random.uniform(25000, 300000), 2)
            try:
                Employee.objects.create(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=fake.unique.email(),
                    phone=fake.phone_number(),
                    gender=random.choice(['Male','Female','Other']),
                    department=dept,
                    role=role,
                    salary=salary,
                    date_of_joining=doj,
                    experience_years=exp_years,
                    location=fake.city()
                )
                created += 1
            except IntegrityError:
                # skip duplicate email
                continue
        self.stdout.write(self.style.SUCCESS(f'Created {created} employees'))
