from django.core.management.base import BaseCommand
from mywebsite.models import User  
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = "Create 10 realistic test users with password 'password123'"

    def handle(self, *args, **kwargs):
        user_types = ['admin', 'agent', 'underwriter', 'claims_officer', 'customer_service', 'finance']
        base_password = "password123"

        for i in range(10):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"{first_name.lower()}.{last_name.lower()}"
            email = f"{username}@example.com"
            phone_number = f"07{random.randint(10000000, 99999999)}"
            national_id = f"NI{random.randint(1000000, 9999999)}"
            employee_id = f"EMP{random.randint(1000, 9999)}"
            user_type = random.choice(user_types)

            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f"User '{username}' already exists. Skipping..."))
                continue

            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                national_id=national_id,
                employee_id=employee_id,
                user_type=user_type,
                password=base_password,
                is_verified=True,
            )
            self.stdout.write(self.style.SUCCESS(f"Created user: {username} ({email})"))

        self.stdout.write(self.style.SUCCESS("10 test users created successfully."))
