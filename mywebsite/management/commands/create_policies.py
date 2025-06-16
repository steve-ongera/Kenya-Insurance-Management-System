from django.core.management.base import BaseCommand
from mywebsite.models import Policy, Customer, InsuranceProduct, Branch, User  # Adjust the import path
from faker import Faker
import random
from decimal import Decimal
from datetime import date, timedelta

fake = Faker()

class Command(BaseCommand):
    help = "Generate 200 insurance policies"

    def handle(self, *args, **kwargs):
        customers = list(Customer.objects.all())
        products = list(InsuranceProduct.objects.all())
        branches = list(Branch.objects.all())
        agents = list(User.objects.filter(user_type='agent'))
        underwriters = list(User.objects.filter(user_type='underwriter'))

        if not all([customers, products, branches, agents, underwriters]):
            self.stdout.write(self.style.ERROR("❌ Make sure customers, products, branches, agents, and underwriters exist."))
            return

        policy_statuses = ['draft', 'active', 'expired', 'cancelled', 'suspended', 'lapsed']
        payment_terms = ['annual', 'semi_annual', 'quarterly', 'monthly']

        for i in range(200):
            customer = random.choice(customers)
            product = random.choice(products)
            branch = random.choice(branches)
            agent = random.choice(agents)
            underwriter = random.choice(underwriters)

            policy_number = f"POL{10000 + i}"
            status = random.choice(policy_statuses)
            start_date = fake.date_between(start_date="-2y", end_date="today")
            duration_days = random.choice([180, 365, 730])
            end_date = start_date + timedelta(days=duration_days)

            sum_insured = Decimal(random.randint(50000, 1000000))
            premium_amount = sum_insured * Decimal(random.uniform(0.01, 0.1))  # 1–10% of sum insured

            policy = Policy.objects.create(
                policy_number=policy_number,
                customer=customer,
                product=product,
                branch=branch,
                agent=agent,
                underwriter=underwriter,
                status=status,
                start_date=start_date,
                end_date=end_date,
                premium_amount=premium_amount.quantize(Decimal('0.01')),
                sum_insured=sum_insured,
                payment_frequency=random.choice(payment_terms),
                policy_conditions=fake.text(max_nb_chars=150),
                special_terms=fake.text(max_nb_chars=100),
                deductible=Decimal(random.randint(1000, 50000)).quantize(Decimal('0.01'))
            )

            self.stdout.write(self.style.SUCCESS(f"✅ Created policy {policy.policy_number} for {customer}"))

        self.stdout.write(self.style.SUCCESS("🎉 200 policies created successfully."))
