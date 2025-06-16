from django.core.management.base import BaseCommand
from mywebsite.models import ReinsuranceContract, InsuranceProduct  # Adjust import path
from faker import Faker
from decimal import Decimal
import random
from datetime import timedelta, date

fake = Faker()

class Command(BaseCommand):
    help = "Generate reinsurance contracts for insurance products"

    def handle(self, *args, **kwargs):
        products = InsuranceProduct.objects.all()
        if not products.exists():
            self.stdout.write(self.style.ERROR("❌ No insurance products found."))
            return

        contract_types = ['quota_share', 'surplus', 'excess_of_loss', 'stop_loss']
        created = 0

        for product in products:
            for _ in range(random.randint(1, 2)):  # Create 1–2 contracts per product
                contract_number = f"RC{fake.unique.random_number(digits=6)}"
                reinsurer_name = fake.company()
                contract_type = random.choice(contract_types)
                effective_date = fake.date_between(start_date="-3y", end_date="today")
                expiry_date = effective_date + timedelta(days=random.randint(180, 1095))  # 6 months to 3 years
                retention_limit = Decimal(random.randint(500000, 5000000))
                reinsurance_rate = Decimal(random.uniform(2.5, 15)).quantize(Decimal('0.01'))

                ReinsuranceContract.objects.create(
                    contract_number=contract_number,
                    reinsurer_name=reinsurer_name,
                    contract_type=contract_type,
                    product=product,
                    effective_date=effective_date,
                    expiry_date=expiry_date,
                    retention_limit=retention_limit,
                    reinsurance_rate=reinsurance_rate,
                    terms_conditions=fake.text(max_nb_chars=300)
                )

                self.stdout.write(self.style.SUCCESS(
                    f"✅ Contract {contract_number} created for {product.name} ({contract_type})"
                ))
                created += 1

        self.stdout.write(self.style.SUCCESS(f"\n🎉 Created {created} reinsurance contracts."))
