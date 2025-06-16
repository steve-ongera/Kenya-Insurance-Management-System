from django.core.management.base import BaseCommand
from mywebsite.models import InsuranceProduct  # Change 'accounts' to your actual app name
import random
from faker import Faker
from decimal import Decimal

fake = Faker()

class Command(BaseCommand):
    help = "Create realistic insurance products"

    def handle(self, *args, **kwargs):
        product_templates = {
            'motor': ['Comprehensive Motor Cover', 'Third-Party Cover'],
            'health': ['Family Health Cover', 'Individual Health Cover'],
            'life': ['Term Life Insurance', 'Whole Life Cover'],
            'property': ['Homeowners Cover', 'Commercial Property Cover'],
            'marine': ['Cargo Insurance', 'Hull Insurance'],
            'aviation': ['Aircraft Hull Cover', 'Passenger Liability'],
            'liability': ['General Liability', 'Professional Indemnity'],
            'travel': ['International Travel Cover', 'Student Travel Plan'],
            'agriculture': ['Crop Insurance', 'Livestock Cover'],
        }

        counter = 1

        for category, products in product_templates.items():
            for product_name in products:
                code = f"{category.upper()}_{counter:03d}"
                description = fake.paragraph(nb_sentences=4)
                minimum_premium = Decimal(random.randint(1000, 10000))
                maximum_coverage = Decimal(random.randint(50000, 1000000))
                commission_rate = Decimal(round(random.uniform(2.5, 15.0), 2))

                if InsuranceProduct.objects.filter(code=code).exists():
                    self.stdout.write(self.style.WARNING(f"Product {code} already exists. Skipping..."))
                    continue

                InsuranceProduct.objects.create(
                    name=product_name,
                    code=code,
                    category=category,
                    description=description,
                    minimum_premium=minimum_premium,
                    maximum_coverage=maximum_coverage,
                    commission_rate=commission_rate
                )

                self.stdout.write(self.style.SUCCESS(f"✅ Created product: {product_name} ({category})"))
                counter += 1

        self.stdout.write(self.style.SUCCESS("🎉 Insurance products created successfully."))
