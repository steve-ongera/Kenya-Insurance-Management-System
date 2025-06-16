from django.core.management.base import BaseCommand
from mywebsite.models import Quotation, Customer, InsuranceProduct, User  # Update import paths
from faker import Faker
from decimal import Decimal
import random
from datetime import timedelta, date

fake = Faker()

class Command(BaseCommand):
    help = "Generate 300 insurance quotations"

    def handle(self, *args, **kwargs):
        customers = list(Customer.objects.all())
        products = list(InsuranceProduct.objects.all())
        agents = list(User.objects.filter(user_type='agent'))

        if not customers or not products or not agents:
            self.stdout.write(self.style.ERROR("❌ Ensure customers, products, and agents exist."))
            return

        statuses = ['draft', 'sent', 'accepted', 'declined', 'expired', 'converted']

        for i in range(300):
            customer = random.choice(customers)
            product = random.choice(products)
            agent = random.choice(agents)

            sum_insured = Decimal(random.randint(100000, 5000000))
            premium_amount = (sum_insured * Decimal(random.uniform(0.01, 0.08))).quantize(Decimal("0.01"))

            quotation = Quotation.objects.create(
                quotation_number=f"QTN{100000 + i}",
                customer=customer,
                product=product,
                agent=agent,
                status=random.choice(statuses),
                valid_until=date.today() + timedelta(days=random.randint(10, 90)),
                premium_amount=premium_amount,
                sum_insured=sum_insured,
                terms_conditions=fake.text(max_nb_chars=200)
            )

            self.stdout.write(self.style.SUCCESS(f"✅ Created quotation {quotation.quotation_number}"))

        self.stdout.write(self.style.SUCCESS("🎉 300 quotations created successfully."))
