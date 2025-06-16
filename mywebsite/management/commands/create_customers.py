from django.core.management.base import BaseCommand
from mywebsite.models import Customer, Branch, User  # Adjust import paths to match your app structure
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

class Command(BaseCommand):
    help = "Create 300 test customers (individual and corporate)"

    def handle(self, *args, **kwargs):
        branches = list(Branch.objects.all())
        agents = list(User.objects.filter(user_type='agent'))

        if not branches or not agents:
            self.stdout.write(self.style.ERROR("❌ You need at least one branch and one agent in the database."))
            return

        for i in range(300):
            customer_type = random.choice(['individual'] * 7 + ['corporate'] * 3)  # 70% individuals, 30% corporate
            customer_number = f"CUST{i+1:05d}"
            phone_number = f"+2547{random.randint(10000000, 99999999)}"
            email = fake.email()
            postal_address = fake.postcode()
            physical_address = fake.address().replace("\n", ", ")
            county = fake.city()
            town = fake.city()
            branch = random.choice(branches)
            agent = random.choice(agents)

            if customer_type == 'individual':
                first_name = fake.first_name()
                last_name = fake.last_name()
                middle_name = fake.first_name()
                gender = random.choice(['M', 'F', 'O'])
                date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=75)
                national_id = f"{random.randint(10000000, 99999999)}"
                passport_number = f"KE{random.randint(1000000, 9999999)}"

                customer = Customer.objects.create(
                    customer_number=customer_number,
                    customer_type='individual',
                    first_name=first_name,
                    last_name=last_name,
                    middle_name=middle_name,
                    gender=gender,
                    date_of_birth=date_of_birth,
                    national_id=national_id,
                    passport_number=passport_number,
                    phone_number=phone_number,
                    email=email,
                    postal_address=postal_address,
                    physical_address=physical_address,
                    county=county,
                    town=town,
                    branch=branch,
                    agent=agent
                )

            else:  # corporate
                company_name = fake.company()
                registration_number = f"REG{random.randint(10000, 99999)}"
                kra_pin = f"A{random.randint(100000000, 999999999)}B"
                business_type = random.choice(['Insurance', 'Finance', 'Retail', 'Transport', 'Construction'])

                customer = Customer.objects.create(
                    customer_number=customer_number,
                    customer_type='corporate',
                    company_name=company_name,
                    registration_number=registration_number,
                    kra_pin=kra_pin,
                    business_type=business_type,
                    phone_number=phone_number,
                    email=email,
                    postal_address=postal_address,
                    physical_address=physical_address,
                    county=county,
                    town=town,
                    branch=branch,
                    agent=agent
                )

            self.stdout.write(self.style.SUCCESS(f"Created customer {customer_number}"))

        self.stdout.write(self.style.SUCCESS("✅ 300 test customers created successfully."))
