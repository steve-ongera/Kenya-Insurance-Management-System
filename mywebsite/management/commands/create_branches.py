from django.core.management.base import BaseCommand
from mywebsite.models import Branch, User  # Adjust 'accounts' to match your app name
from faker import Faker
import random

fake = Faker()

KENYAN_TOWNS_AND_COUNTIES = [
    ("Nairobi", "Nairobi"),
    ("Mombasa", "Mombasa"),
    ("Kisumu", "Kisumu"),
    ("Nakuru", "Nakuru"),
    ("Eldoret", "Uasin Gishu"),
    ("Thika", "Kiambu"),
    ("Nyeri", "Nyeri"),
    ("Meru", "Meru"),
    ("Embu", "Embu"),
    ("Machakos", "Machakos"),
    ("Kericho", "Kericho"),
    ("Kakamega", "Kakamega"),
    ("Kitale", "Trans Nzoia"),
    ("Garissa", "Garissa"),
    ("Isiolo", "Isiolo"),
    ("Narok", "Narok"),
    ("Lamu", "Lamu"),
    ("Voi", "Taita Taveta"),
    ("Homa Bay", "Homa Bay"),
    ("Nanyuki", "Laikipia")
]

class Command(BaseCommand):
    help = "Create 20 insurance branches in Kenya"

    def handle(self, *args, **kwargs):
        for i in range(20):
            town, county = KENYAN_TOWNS_AND_COUNTIES[i]
            name = f"{town} Branch"
            code = f"BR{i+1:03d}"
            address = fake.address().replace("\n", ", ")
            phone_number = f"+2547{random.randint(10000000, 99999999)}"
            email = f"{town.lower()}@insurance.co.ke"

            # Optionally assign a random existing user as manager
            managers = User.objects.filter(is_active=True)
            manager = random.choice(managers) if managers.exists() else None

            if Branch.objects.filter(code=code).exists():
                self.stdout.write(self.style.WARNING(f"Branch {code} already exists. Skipping..."))
                continue

            branch = Branch.objects.create(
                name=name,
                code=code,
                address=address,
                county=county,
                town=town,
                phone_number=phone_number,
                email=email,
                manager=manager,
            )
            self.stdout.write(self.style.SUCCESS(f"Created branch: {branch.name} ({branch.code})"))

        self.stdout.write(self.style.SUCCESS("✅ 20 branches created successfully."))
